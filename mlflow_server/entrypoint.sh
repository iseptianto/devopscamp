#!/bin/bash

set -e

echo "▶️ Waiting for PostgreSQL to be available..."
until nc -z -v -w30 $MLFLOW_DB_HOST 5432
do
  echo "⏳ Waiting for database connection..."
  sleep 5
done

echo "✅ PostgreSQL is available - starting MLflow server"

exec mlflow server \
  --backend-store-uri postgresql://$MLFLOW_DB_USER:$MLFLOW_DB_PASSWORD@$MLFLOW_DB_HOST:5432/$MLFLOW_DB_NAME \
  --default-artifact-root s3://$MLFLOW_S3_BUCKET/ \
  --host 0.0.0.0 \
  --port 5001
