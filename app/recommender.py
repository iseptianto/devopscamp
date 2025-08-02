"""
Modul ini berisi semua logika inti untuk sistem rekomendasi pariwisata.
Tugasnya adalah memuat model dan data yang telah dilatih, kemudian menyediakan
berbagai fungsi untuk menghasilkan rekomendasi berdasarkan input yang diterima dari API.
"""

# --- Import Library ---
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from geopy.distance import geodesic

# Load model & metadata
# Pastikan path ini benar relatif terhadap direktori kerja saat menjalankan api.py
# --- Memuat Model & Metadata ---
# Path ini relatif terhadap direktori kerja utama (tempat api.py dijalankan).
# Model-model ini dihasilkan oleh notebook 'tourism.ipynb'.

# Matriks prediksi hasil dari model Collaborative Filtering
prediction_matrix = pickle.load(open("app/models/prediction_matrix.pkl", "rb"))
# Encoder untuk mengubah User_Id menjadi indeks numerik
user_encoder = pickle.load(open("app/models/user_encoder.pkl", "rb"))
# Encoder untuk mengubah Place_Id menjadi indeks numerik
place_encoder = pickle.load(open("app/models/place_encoder.pkl", "rb"))
# Metadata untuk setiap tempat wisata
place_metadata = pd.read_csv("app/models/place_metadata.csv")

# Matriks similaritas berbasis konten (kategori & kota)
with open("app/models/content_similarity.pkl", "rb") as f:
    similarity_matrix = pickle.load(f)

# Kode di bawah ini seharusnya berada di skrip terpisah untuk persiapan data/model,
# bukan di sini karena akan dijalankan setiap kali aplikasi diimpor.
# with open("user_encoder.pkl", "wb") as f:
#     pickle.dump(user_encoder, f)
# with open("place_encoder.pkl", "wb") as f:
#     pickle.dump(place_encoder, f)
# with open("place_metadata.csv", "wb") as f:
#     place_metadata.to_csv(f, index=False)

# --- Logging untuk verifikasi saat startup ---
# Pesan ini akan muncul di log server saat aplikasi pertama kali dijalankan.
# print("✅ Data berhasil dimuat!")
# print("User ID yang tersedia (user_encoder.classes_):", user_encoder.classes_[:10])
# print("Place ID yang tersedia (place_encoder.classes_):", place_encoder.classes_[:10])
# print("Metadata sample Place_Id:", place_metadata['Place_Id'].unique()[:10])

def convert_numpy(obj):
    """
    Fungsi utilitas untuk mengonversi tipe data NumPy secara rekursif
    menjadi tipe data Python standar agar bisa di-serialize ke format JSON.

    Args:
        obj: Objek Python yang mungkin berisi tipe data NumPy.

    Returns:
        Objek dengan semua tipe data NumPy telah dikonversi.
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return obj
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    else:
        return obj

def show_similar_places(place_name, top_n=5):
    """
    Mencari tempat wisata yang mirip berdasarkan kemiripan konten (kategori & kota).

    Args:
        place_name (str): Nama tempat wisata yang ingin dicari kemiripannya.
        top_n (int): Jumlah tempat mirip yang ingin ditampilkan.

    Returns:
        list: Daftar dictionary berisi informasi tempat-tempat yang mirip.
    """
    if not place_name:
        return []

    # Cari yang mengandung teks tersebut (lebih fleksibel)
    # Cari tempat yang namanya mengandung teks yang diberikan (case-insensitive)
    match = place_metadata[place_metadata['Place_Name'].str.lower().str.contains(place_name.lower())]

    # Jika tidak ditemukan
    # Jika tidak ada yang cocok, kembalikan list kosong
    if match.empty:
        return []

    # Ambil index tempat pertama yang cocok
    idx = match.index[0]

    # Hitung similarity
    # Ambil skor similaritas untuk tempat tersebut dari matriks
    sim_scores = list(enumerate(similarity_matrix[idx]))
    # Urutkan berdasarkan skor similaritas (dari tertinggi ke terendah)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    # Buat hasil rekomendasi
    # Siapkan hasil rekomendasi
    similar_places = []
    for i, score in sim_scores:
        row = place_metadata.iloc[i]
        similar_places.append({
            "Place_Id": row["Place_Id"],
            "Place_Name": row["Place_Name"],
            "Category": row["Category"],
            "City": row["City"],
            "Similarity_Score": float(round(score, 3))
        })

    return similar_places

def get_user_profile(user_id):
    """
    Membuat profil preferensi kategori seorang user berdasarkan rating yang pernah diberikan.

    Args:
        user_id (str atau int): ID dari user.

    Returns:
        dict: Dictionary berisi frekuensi kategori yang disukai user.
    """
    try:
        # Ubah user_id string menjadi index numerik
        user_idx = user_encoder.transform([int(user_id)])[0]
    except:
        # Jika user tidak ditemukan, kembalikan dictionary kosong
        return {}
    # Ambil semua prediksi rating untuk user ini
    user_ratings = prediction_matrix[user_idx]
    # Urutkan tempat dari rating tertinggi
    top_places = np.argsort(user_ratings)[::-1]
    # Ambil 10 Place_Id teratas dan ubah kembali dari index ke ID asli
    top_place_ids = place_encoder.inverse_transform(top_places[:10])
    # Cari kategori dari tempat-tempat tersebut
    top_categories = place_metadata[place_metadata['Place_Id'].isin(top_place_ids)]['Category']
    # Hitung frekuensi setiap kategori dan kembalikan sebagai dictionary
    return top_categories.value_counts().to_dict()

def hybrid_recommend(user_id, top_n=5):
    """
    Memberikan rekomendasi hybrid dengan memfilter hasil Collaborative Filtering (CF)
    berdasarkan kategori favorit user (Content-Based).

    Args:
        user_id (str atau int): ID dari user.
        top_n (int): Jumlah rekomendasi yang diinginkan.

    Returns:
        list: Daftar rekomendasi tempat wisata.
    """
    # Dapatkan 20 rekomendasi awal dari CF
    cf_result = recommend_user(user_id, top_n=20)
    # Dapatkan profil kategori user
    categories = get_user_profile(user_id)
    # Tentukan kategori favorit
    favorite_cat = max(categories, key=categories.get) if categories else None
    # Filter hasil CF berdasarkan kategori favorit
    hybrid_result = [place for place in cf_result if place['Category'] == favorite_cat]
    # Jika ada hasilnya, kembalikan top_n. Jika tidak, kembalikan hasil CF asli.
    return hybrid_result[:top_n] if hybrid_result else cf_result[:top_n]

def find_nearby_places(lat, lon, radius_km=20):
    """
    Mencari tempat wisata terdekat dari titik koordinat (lat, lon) dalam radius tertentu.

    Args:
        lat (float): Latitude dari lokasi saat ini.
        lon (float): Longitude dari lokasi saat ini.
        radius_km (float): Radius pencarian dalam kilometer.

    Returns:
        list: Daftar tempat wisata terdekat, diurutkan berdasarkan jarak.
    """
    nearby = []
    for _, row in place_metadata.iterrows():
        # Hitung jarak geosentris antara dua titik
        loc = (row['Lat'], row['Long'])
        distance = geodesic((lat, lon), loc).km
        if distance <= radius_km:
            nearby.append({
                'Place_Id': row['Place_Id'],
                'Place_Name': row['Place_Name'],
                'City': row['City'],
                'Distance_km': round(distance, 2)
            })
    # Urutkan hasilnya berdasarkan jarak terdekat
    return sorted(nearby, key=lambda x: x['Distance_km'])

def recommend_user(user_id, top_n=5):
    """
    Memberikan rekomendasi tempat wisata untuk user berdasarkan Collaborative Filtering.

    Args:
        user_id (str atau int): ID dari user.
        top_n (int): Jumlah rekomendasi yang diinginkan.

    Returns:
        list: Daftar rekomendasi tempat wisata.
    """
    try:
        # Konversi user_id dari string (dari API) ke integer
        user_id = int(user_id)
        print(f"🔍 Mencoba rekomendasi untuk user_id: {user_id}")

        # Pastikan user_id ada di encoder
        # Ubah user_id menjadi index numerik
        if user_id not in user_encoder.classes_:
            print(f"⚠️ User ID {user_id} tidak ada di dalam data training.")
            return []
        user_idx = user_encoder.transform([user_id])[0]
        print(f"✅ User ditemukan dengan index: {user_idx}")
    except Exception as e:
        print(f"❌ User ID {user_id} tidak ditemukan di user_encoder. Error: {e}")
        return [] # Kembalikan list kosong jika user tidak ditemukan

    try:
        # Ambil prediksi rating untuk user tersebut
        user_ratings = prediction_matrix[user_idx]
        print("📊 Contoh prediksi rating user:", user_ratings[:10])

        # Urutkan dari skor tertinggi
        # Urutkan index tempat berdasarkan skor prediksi dari tertinggi ke terendah
        top_items = np.argsort(user_ratings)[::-1]

        recommendations = []
        for idx in top_items:
            try:
                # Ubah kembali index tempat menjadi Place_Id asli
                place_id = place_encoder.inverse_transform([idx])[0]
                # Cari metadata tempat berdasarkan Place_Id
                place_info = place_metadata[place_metadata['Place_Id'] == place_id]

                # Jika metadata ditemukan
                if not place_info.empty:
                    row = place_info.iloc[0]
                    # Tambahkan ke daftar rekomendasi
                    recommendations.append({
                        'Place_Id': place_id,
                        'Place_Name': row['Place_Name'],
                        'Category': row['Category'],
                        'City': row['City']
                    })
                    # Log ini akan muncul di terminal server, bukan di browser
                    print(f"✅ Menambahkan tempat: {row['Place_Name']} (ID: {place_id})")

                # Hentikan jika sudah mencapai jumlah top_n yang diinginkan
                if len(recommendations) >= top_n:
                    break

            except Exception as e:
                # Tangani jika ada error saat memproses satu item
                print(f"⚠️ Gagal proses place index {idx}: {e}")

        if not recommendations:
            print("⚠️ Tidak ada tempat yang direkomendasikan.")
        return recommendations

    except Exception as e:
        # Tangani jika ada error saat proses rekomendasi utama
        print(f"❌ Terjadi kesalahan saat menghasilkan rekomendasi: {e}")
        return []

