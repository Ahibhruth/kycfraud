import joblib
import numpy as np

# Load scaler & features
scaler = joblib.load("app/model/scaler.pkl")
selected_features = joblib.load("app/model/features.pkl")

def preprocess_input(data: dict):
    """
    Converts incoming JSON to model-ready numpy array.
    """
    processed = []

    for feature in selected_features:
        processed.append(float(data.get(feature, 0)))  # default 0

    processed = np.array(processed).reshape(1, -1)

    # Scale
    processed = scaler.transform(processed)
    return processed
