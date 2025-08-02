FROM python:3.9-slim

WORKDIR /mlflow

RUN pip install --no-cache-dir mlflow boto3 psycopg2-binary

EXPOSE 5001

CMD ["mlflow", "server", 
     "--backend-store-uri", "postgresql://mlflow:mlflow@mlflow_db:5432/mlflow", 
     "--default-artifact-root", "s3://mlflow/", 
     "--host", "0.0.0.0", 
     "--port", "5001"]
