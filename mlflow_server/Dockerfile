FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir mlflow psycopg2-binary boto3

CMD ["mlflow", "server", "--backend-store-uri", "postgresql://mlflow:mlflow@mlflow_db:5432/mlflow", "--default-artifact-root", "s3://mlflow/", "--host", "0.0.0.0", "--port", "5001"]

