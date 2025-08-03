from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI(title="Indonesian Tourism Recommendation API")

# Load models
content_similarity = joblib.load("models/model_tourism/content_similarity.pkl")
place_encoder = joblib.load("models/model_tourism/place_encoder.pkl")
prediction_matrix = joblib.load("models/model_tourism/prediction_matrix.pkl")
user_encoder = joblib.load("models/model_tourism/user_encoder.pkl")

@app.get("/")
def root():
    return {"message": "Tourism recommendation API is up!"}

@app.get("/recommend/{user_id}")
def recommend_places(user_id: int, top_k: int = 5):
    if user_id >= prediction_matrix.shape[0]:
        return {"error": "Invalid user_id"}
    scores = prediction_matrix[user_id]
    top_indices = np.argsort(scores)[::-1][:top_k]
    recommended_places = [str(i) for i in top_indices]
    return {"user_id": user_id, "recommendations": recommended_places}
