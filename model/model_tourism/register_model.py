import mlflow
import joblib
import os

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow_server:5001"))
mlflow.set_experiment("tourism-indonesia")

with mlflow.start_run():
    for file in ["prediction_matrix.pkl", "user_encoder.pkl", "place_encoder.pkl", "content_similarity.pkl"]:
        mlflow.log_artifact(file)

    mlflow.log_metric("dummy_accuracy", 0.9)
