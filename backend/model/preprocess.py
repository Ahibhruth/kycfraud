# preprocess.py

import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_dataset(csv_path):

    df = pd.read_csv(csv_path)

    # Required
    required = [
        "Name_clean", "Address_clean", "Gender_clean",
        "Document_type_clean", "Document_Number",
        "Fraud_Risk_Score", "Fraud_Risk_Level"
    ]

    for col in required:
        if col not in df.columns:
            raise KeyError(f"Missing column: {col}")

    # ✅ Label encoders
    le_gender = LabelEncoder()
    le_doc = LabelEncoder()

    df["Gender_encoded"] = le_gender.fit_transform(df["Gender_clean"])
    df["Doc_encoded"] = le_doc.fit_transform(df["Document_type_clean"])

    # ✅ Numeric features
    df["Name_clean"] = df["Name_clean"].astype(str)
    df["Address_clean"] = df["Address_clean"].astype(str)
    df["Document_Number"] = df["Document_Number"].astype(str)

# ✅ Safe length calculation
    df["Name_Length"] = df["Name_clean"].str.len()
    df["Address_Length"] = df["Address_clean"].str.len()

    df["Name_Freq"] = 1
    df["Address_Freq"] = 1
    df["Group_Size"] = 1

    feature_cols = [
        "Name_Length",
        "Address_Length",
        "Name_Freq",
        "Address_Freq",
        "Group_Size",
        "Gender_encoded",
        "Doc_encoded",
        "Fraud_Risk_Score"
    ]

    X = df[feature_cols]

    # ✅ Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ✅ Save encoders for API
    joblib.dump({
        "le_gender": le_gender,
        "le_doc": le_doc,
        "scaler": scaler
    }, "model/label_encoders.pkl")

    print("✅ Encoders saved successfully!")

    return df, X_scaled
