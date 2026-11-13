from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = Path("/app/ml/models/churn_model.pkl")
if not MODEL_PATH.exists():
    MODEL_PATH = BASE_DIR / "ml" / "models" / "churn_model.pkl"

model = None


def get_model():

    global model

    if model is None:
        model = joblib.load(MODEL_PATH)

    return model


def predict_churn(features):

    model = get_model()

    prediction = int(model.predict([features])[0])
    result = {
        "prediction": prediction,
        "churn_prediction": prediction,
    }
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba([features])[0]
        result["probability"] = round(float(probs[1]), 4)

    return result
