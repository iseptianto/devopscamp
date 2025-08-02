import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pickle

def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def train_and_log_new_model():
    print("🚀 Training new model and logging to MLflow...")
    mlflow.set_tracking_uri("http://mlflow_server:5001")
    mlflow.set_experiment("iris_training")

    with mlflow.start_run():
        iris = load_iris()
        X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target)

        model = LogisticRegression(max_iter=200)
        model.fit(X_train, y_train)
        acc = model.score(X_test, y_test)

        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, artifact_path="model")
        print(f"✅ Model trained and logged with accuracy: {acc:.4f}")

def load_existing_models():
    print("🧠 Loading pre-trained models...")
    content_similarity = load_model("model/content_similarity.pkl")
    place_encoder = load_model("model/place_encoder.pkl")
    prediction_matrix = load_model("model/prediction_matrix.pkl")
    user_encoder = load_model("model/user_encoder.pkl")

    print("✅ Loaded all models successfully!")
    try:
        print(content_similarity.shape)
    except:
        print(content_similarity.keys())

if __name__ == "__main__":
    train_and_log_new_model()
    load_existing_models()
