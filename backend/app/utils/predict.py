import joblib
from .preprocess import preprocess_input

model = joblib.load("app/model/fraud_model.pkl")

def predict_fraud(data: dict):
    processed = preprocess_input(data)
    prediction = model.predict(processed)[0]

    return {
        "fraud_prediction": int(prediction),
        "message": "Fraud Transaction" if prediction == 1 else "Legitimate Transaction"
    }
