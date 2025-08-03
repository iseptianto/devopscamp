import mlflow
import os
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://mlflow_minio:9000'
os.environ['AWS_ACCESS_KEY_ID'] = 'minioadmin'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minioadmin'


mlflow.set_tracking_uri("http://mlflow_server:5001")
mlflow.set_experiment("tourism-indonesia")

with mlflow.start_run():
    for file in ["prediction_matrix.pkl", "user_encoder.pkl", "place_encoder.pkl", "content_similarity.pkl"]:
        mlflow.log_artifact(file)

    mlflow.log_metric("dummy_accuracy", 0.9)

import boto3

boto3.client(
    's3',
    endpoint_url='http://mlflow_minio:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
    region_name='us-east-1'  # bebas
)
