FROM python:3.9

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y curl
RUN pip install --no-cache-dir -r app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]


