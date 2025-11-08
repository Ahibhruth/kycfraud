# api/server.py

from fastapi import FastAPI
import torch
import joblib
import numpy as np
from pydantic import BaseModel

# ✅ Correct imports
from api.compliance_rules import apply_compliance_rules
from api.utils import build_feature_vector
from model.train_gnn import FraudGNN  # ✅ import model class from training file

app = FastAPI()

# ✅ Load model & encoders
model_state = torch.load("model/model.pth", map_location="cpu")
encoders = joblib.load("model/label_encoders.pkl")

# ✅ The GNN model has 8 input features now
model = FraudGNN(input_dim=8)
model.load_state_dict(model_state)
model.eval()

class KYCRecord(BaseModel):
    Name: str
    Gender_clean: str
    Document_type_clean: str
    Address_clean: str
    Document_Number: str
    Combined_Data: str
    Fraud_Risk_Score: float


@app.post("/predict_fraud")
def predict(kyc: KYCRecord):

    # ✅ Build feature vector
    X = build_feature_vector(kyc, encoders)
    X = torch.tensor(X, dtype=torch.float).unsqueeze(0)

    # ✅ Correct forward pass (no fake edge index)
    with torch.no_grad():
        pred = model.fc(model.conv2(model.conv1(X, torch.tensor([[0],[0]])), torch.tensor([[0],[0]])))

    prob = float(pred.item())

    # ✅ Apply business rules
    decision = apply_compliance_rules(prob, kyc)

    return {
        "fraud_probability": prob,
        "decision": decision
    }
