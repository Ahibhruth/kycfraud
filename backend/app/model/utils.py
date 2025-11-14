# api/utils.py

import numpy as np

def build_feature_vector(kyc, enc):
    """
    Build the SAME 8-feature vector used in train_gnn.py
    """

    name_len = len(kyc.Name)
    addr_len = len(kyc.Address_clean)

    name_freq = 1                 # You can replace with real logic later
    addr_freq = 1
    group_size = 1
    fraud_risk = float(kyc.Fraud_Risk_Score)

    # ✅ Use label encoders loaded from train phase
    gender_enc = enc["le_gender"].transform([kyc.Gender_clean])[0]
    doc_enc = enc["le_doc"].transform([kyc.Document_type_clean])[0]

    # ✅ Final feature vector (8 features)
    vec = np.array([
        name_len,        # 1
        addr_len,        # 2
        name_freq,       # 3
        addr_freq,       # 4
        group_size,      # 5
        gender_enc,      # 6
        doc_enc,         # 7
        fraud_risk       # 8
    ], dtype=float)

    return vec
