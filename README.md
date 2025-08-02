# Tourism Recommendation API

API ini menyediakan sistem rekomendasi tempat pariwisata di Indonesia. Dibangun menggunakan Flask, API ini mengekspos beberapa model rekomendasi, termasuk *Collaborative Filtering*, *Content-Based*, dan *Hybrid*, serta fungsionalitas tambahan seperti pencarian tempat terdekat.

Proyek ini juga dilengkapi dengan konfigurasi untuk deployment menggunakan Docker dan Kubernetes.

## Fitur Utama

- **Rekomendasi Collaborative Filtering**: Memberikan rekomendasi berdasarkan kemiripan perilaku antar pengguna.
- **Rekomendasi Hybrid**: Menggabungkan kekuatan Collaborative Filtering dengan preferensi kategori pengguna (Content-Based) untuk hasil yang lebih relevan.
- **Pencarian Tempat Serupa**: Menemukan tempat wisata yang mirip berdasarkan kemiripan konten (kategori dan kota).
- **Pencarian Tempat Terdekat**: Menemukan tempat wisata dalam radius tertentu dari lokasi geografis pengguna.
- **Profil Preferensi Pengguna**: Menganalisis riwayat rating pengguna untuk menentukan kategori favorit mereka.
- **Siap Untuk Kubernetes**: Dilengkapi dengan *health check endpoint* (`/health`) untuk integrasi dengan Kubernetes.

## Teknologi yang Digunakan

- **Backend**: Python, Flask
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Geospatial**: Geopy
- **Deployment**: Docker, Kubernetes

---

## Panduan API Endpoint

Berikut adalah daftar endpoint yang tersedia:

| Endpoint              | Metode | Deskripsi                                     | Parameter Kueri                               | Contoh Respons Sukses                                                              |
| :-------------------- | :----- | :-------------------------------------------- | :-------------------------------------------- | :--------------------------------------------------------------------------------- |
| `/`                   | `GET`  | Cek status dasar API.                         | -                                             | `Tourism Recommendation API aktif!`                                                |
| `/health`             | `GET`  | Endpoint *health check* untuk Kubernetes.     | -                                             | `{"status": "ok"}`                                                                 |
| `/recommend/user`     | `GET`  | Rekomendasi Collaborative Filtering.          | `user_id` (wajib)                             | `[{"Place_Id": 123, "Place_Name": "Monas", ...}]`                                   |
| `/recommend/hybrid`   | `GET`  | Rekomendasi Hybrid (CF + Content-based).      | `user_id` (wajib)                             | `[{"Place_Id": 456, "Place_Name": "Taman Mini", ...}]`                              |
| `/places/nearby`      | `GET`  | Mencari tempat wisata terdekat.               | `lat`, `lon` (wajib), `radius` (opsional)     | `[{"Place_Id": 789, "Place_Name": "Ancol", "Distance_km": 5.2, ...}]`               |
| `/user/profile`       | `GET`  | Mendapatkan profil preferensi kategori user.  | `user_id` (wajib)                             | `{"Budaya": 5, "Cagar Alam": 3, ...}`                                              |
| `/places/similar`     | `GET`  | Mencari tempat yang mirip berdasarkan nama.   | `place_name` (wajib)                          | `[{"Place_Id": 101, "Place_Name": "Keraton Yogyakarta", "Similarity_Score": 0.85}]` |

---

## Contoh Penggunaan API

Berikut adalah contoh detail untuk setiap endpoint, termasuk contoh permintaan menggunakan `curl` dan contoh respons JSON.

### 1. Rekomendasi untuk User (Collaborative Filtering)
Memberikan rekomendasi tempat wisata berdasarkan histori rating pengguna lain yang memiliki kemiripan perilaku.

*   **Endpoint**: `GET /recommend/user`
*   **Parameter**:
    *   `user_id` (wajib): ID unik pengguna.
*   **Contoh Permintaan**:
    ```bash
    curl -X GET "http://localhost:5000/recommend/user?user_id=101"
    ```
*   **Contoh Respons Sukses**:
    ```json
    [
      {
        "Category": "Budaya",
        "City": "Jakarta Pusat",
        "Place_Id": 123,
        "Place_Name": "Monumen Nasional"
      },
      {
        "Category": "Taman Hiburan",
        "City": "Jakarta Utara",
        "Place_Id": 150,
        "Place_Name": "Dunia Fantasi"
      }
    ]
    ```

### 2. Rekomendasi Hybrid (Collaborative + Content-based)
Menggabungkan hasil Collaborative Filtering dengan preferensi kategori favorit pengguna untuk memberikan rekomendasi yang lebih personal.

*   **Endpoint**: `GET /recommend/hybrid`
*   **Parameter**:
    *   `user_id` (wajib): ID unik pengguna.
*   **Contoh Permintaan**:
    ```bash
    curl -X GET "http://localhost:5000/recommend/hybrid?user_id=101"
    ```
*   **Contoh Respons Sukses**:
    ```json
    [
      {
        "Category": "Taman Hiburan",
        "City": "Jakarta Timur",
        "Place_Id": 456,
        "Place_Name": "Taman Mini Indonesia Indah"
      }
    ]
    ```

### 3. Tempat Wisata Serupa (Content-Based)
Menemukan tempat-tempat wisata yang memiliki kemiripan konten (berdasarkan kategori dan kota) dengan tempat yang diberikan.

*   **Endpoint**: `GET /places/similar`
*   **Parameter**:
    *   `place_name` (wajib): Nama tempat wisata sebagai acuan.
*   **Contoh Permintaan**:
    ```bash
    curl -X GET "http://localhost:5000/places/similar?place_name=Pantai%20Kuta"
    ```
*   **Contoh Respons Sukses**:
    ```json
    [
      {
        "Category": "Bahari",
        "City": "Badung",
        "Place_Id": 201,
        "Place_Name": "Pantai Legian",
        "Similarity_Score": 0.95
      }
    ]
    ```

### 4. Tempat Wisata Terdekat
Mencari tempat wisata yang berada dalam radius tertentu dari lokasi geografis pengguna.

*   **Endpoint**: `GET /places/nearby`
*   **Parameter**:
    *   `lat` (wajib): Latitude lokasi pengguna.
    *   `lon` (wajib): Longitude lokasi pengguna.
    *   `radius` (opsional, default: 10): Jarak radius pencarian dalam kilometer.
*   **Contoh Permintaan**:
    ```bash
    curl -X GET "http://localhost:5000/places/nearby?lat=-7.2756&lon=112.6426&radius=10"
    ```
*   **Contoh Respons Sukses**:
    ```json
    [
      {
        "City": "Surabaya",
        "Distance_km": 3.5,
        "Place_Id": 301,
        "Place_Name": "Tugu Pahlawan"
      }
    ]
    ```

### 5. Profil Preferensi Pengguna
Menganalisis histori rating pengguna untuk menampilkan kategori wisata yang paling sering ia sukai.

*   **Endpoint**: `GET /user/profile`
*   **Parameter**:
    *   `user_id` (wajib): ID unik pengguna.
*   **Contoh Permintaan**:
    ```bash
    curl -X GET "http://localhost:5000/user/profile?user_id=101"
    ```
*   **Contoh Respons Sukses**:
    ```json
    {
      "Budaya": 8,
      "Taman Hiburan": 5,
      "Cagar Alam": 2
    }
    ```
---

## Instalasi Lokal

1.  **Clone Repositori**
    ```bash
    git clone <URL_REPOSITORI>
    cd tourism-api
    ```

2.  **Buat dan Aktifkan Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # Untuk Windows: venv\Scripts\activate
    ```

3.  **Install Dependensi**
    Pastikan Anda memiliki file `requirements.txt` di direktori root.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Siapkan Model**
    Pastikan semua file model (`.pkl`) dan data (`.csv`) yang diperlukan sudah ada di dalam direktori `app/models/`.

5.  **Jalankan Aplikasi**
    ```bash
    python api.py
    ```
    API akan berjalan di `http://127.0.0.1:5000`.

---

## Deployment dengan Docker & Kubernetes

### 1. Build Docker Image

Pastikan Anda memiliki `Dockerfile` di direktori root.
```bash
# Ganti 'nama-registry/tourism-api:v1' dengan nama image Anda
docker build -t nama-registry/tourism-api:v1 .
```

### 2. Push Image ke Registry

```bash
docker push nama-registry/tourism-api:v1
```

### 3. Konfigurasi Deployment Kubernetes

Buka file `deployment.yaml` dan ubah nilai `image` agar sesuai dengan image yang baru saja Anda push.

```yaml
# deployment.yaml

...
      containers:
      - name: tourism-api-container
        # GANTI BARIS INI
        image: nama-registry/tourism-api:v1
...
```

### 4. Terapkan ke Klaster Kubernetes

```bash
kubectl apply -f deployment.yaml
```

### 5. Akses Aplikasi

Service yang dibuat dalam `deployment.yaml` bertipe `ClusterIP`, artinya hanya dapat diakses dari dalam klaster. Untuk mengujinya dari mesin lokal Anda, gunakan `port-forward`:

```bash
# Dapatkan nama salah satu pod
kubectl get pods

# Lakukan port-forward (ganti 'nama-pod-anda' dengan nama dari perintah sebelumnya)
kubectl port-forward <nama-pod-anda> 8080:5000
```

Sekarang Anda dapat mengakses API melalui `http://localhost:8080` dari mesin lokal Anda. Untuk eksposur eksternal permanen, pertimbangkan untuk mengubah tipe Service menjadi `NodePort` atau `LoadBalancer`.

---

## Struktur Proyek

```
tourism-api/
├── app/
│   ├── __init__.py
│   ├── recommender.py   # Logika inti sistem rekomendasi
│   └── models/          # Direktori untuk menyimpan model .pkl dan data .csv
├── api.py               # File utama API Flask
├── deployment.yaml      # Manifest deployment Kubernetes
├── Dockerfile           # Konfigurasi untuk membangun image Docker
├── requirements.txt     # Daftar dependensi Python
└── README.md            # Dokumentasi ini
```