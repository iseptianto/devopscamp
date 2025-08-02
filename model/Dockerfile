# model/Dockerfile

FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir pandas numpy scikit-learn

CMD ["python", "train_model.py"]
