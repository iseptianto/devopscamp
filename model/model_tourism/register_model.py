import mlflow
import joblib
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow_server:5001")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("tourism-indonesia")

with mlflow.start_run():
    model = joblib.load("model_tourism.pkl")  # ganti sesuai nama file kamu

    # log model ke mlflow
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="tourism-classifier"
    )

    # log metric dummy aja biar gak kosong
    mlflow.log_metric("dummy_accuracy", 0.9)
