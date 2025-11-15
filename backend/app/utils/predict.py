import joblib
import os
from utils.preprocessing import preprocess_dummy_input

MODEL_DIR = "model/"

model = joblib.load(os.path.join(MODEL_DIR, "fraud_model.pkl"))

def classify_risk(prob):
    if prob < 33:
        return "Low"
    elif prob < 66:
        return "Medium"
    else:
        return "High"


def run_model_prediction():
    """
    Runs prediction using ML model.
    Dummy numeric inputs are used now.
    """

    X = preprocess_dummy_input()

    prob = float(model.predict_proba(X)[0][1]) * 100
    prob = round(prob, 2)

    risk = classify_risk(prob)
    confidence = round(100 - prob, 2)

    return {
        "fraud_probability": prob,
        "fraud_risk": risk,
        "confidence": confidence
    }
