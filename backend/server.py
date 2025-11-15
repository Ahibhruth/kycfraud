from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import datetime
import os
from PIL import Image
import io

from utils.prediction import run_model_prediction

app = FastAPI(title="AI-Powered KYC Verification API")

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all (or restrict to your frontend domain)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log file creation
LOG_FILE = "data/kyc_audit_log.csv"
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=[
        "Timestamp", "Name", "Document_Number",
        "Fraud_Risk_Level", "Fraud_Probability", "Confidence"
    ]).to_csv(LOG_FILE, index=False)


@app.post("/api/verify-kyc")
async def verify_kyc(
    id_image: UploadFile = File(...),
    selfie_image: UploadFile = File(...),
    name: str = Form(...),
    document_number: str = Form(...)
):
    # -----------------------------
    # Step 1: Validate Images
    # -----------------------------
    try:
        id_img = Image.open(io.BytesIO(await id_image.read()))
        selfie_img = Image.open(io.BytesIO(await selfie_image.read()))
    except Exception:
        return JSONResponse(
            content={"status": "Error", "message": "Invalid image format"},
            status_code=400
        )

    # -----------------------------
    # Step 2: Run ML Prediction
    # -----------------------------
    pred_result = run_model_prediction()

    fraud_prob = pred_result["fraud_probability"]
    fraud_risk = pred_result["fraud_risk"]
    confidence = pred_result["confidence"]

    # -----------------------------
    # Step 3: Log Entry
    # -----------------------------
    log_entry = pd.DataFrame([{
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "Document_Number": document_number,
        "Fraud_Risk_Level": fraud_risk,
        "Fraud_Probability": fraud_prob,
        "Confidence": confidence
    }])

    log_entry.to_csv(LOG_FILE, mode="a", header=False, index=False)

    # -----------------------------
    # Step 4: Response to Frontend
    # -----------------------------
    return {
        "status": "Verified" if fraud_risk == "Low" else "Not Verified",
        "name": name,
        "document_number": document_number,
        "fraud_risk_level": fraud_risk,
        "fraud_probability": f"{fraud_prob}%",
        "confidence": f"{confidence}%",
        "message": "KYC Verification Completed"
    }


@app.get("/")
def home():
    return {"message": "KYC Verification API is running!"}
