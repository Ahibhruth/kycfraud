def apply_compliance_rules(prob, req):
    if prob > 0.85:
        return "BLOCK – High Fraud Risk"

    if prob > 0.60:
        return "REVIEW – Manual KYC Required"

    if req.Fraud_Risk_Score > 0.7:
        return "REVIEW – Rule Based Trigger"

    return "ALLOW"
