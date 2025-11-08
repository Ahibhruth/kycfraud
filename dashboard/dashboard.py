import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from components.stats_cards import show_stats_cards
from components.fraud_table import show_fraud_table
from components.risk_graph import show_risk_graph

API_URL = "http://127.0.0.1:8000/predict_fraud"

st.set_page_config(page_title="AML/KYC Fraud Monitoring", layout="wide")

st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("KYC + AML Fraud Monitoring Dashboard 🔍")

tab1, tab2, tab3 = st.tabs(["📡 Real-Time Screening", "📊 Fraud Analytics", "🕸 Network Graph"])

# ============================
# ✅ TAB 1 — REAL-TIME SCREENING
# ============================
with tab1:
    st.header("Real-Time KYC Screening")

    with st.form("kyc_form"):
        name = st.text_input("Full Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        doc_type = st.selectbox("Document Type", ["Aadhar", "PAN", "Passport", "Driving License"])
        address = st.text_area("Address")
        doc_number = st.text_input("Document Number")
        data = st.text_area("Combined Data (auto-generated or manual)")
        rule_score = st.slider("Rule-based Risk Score", 0.0, 1.0)

        submitted = st.form_submit_button("Predict Fraud")

    if submitted:
        payload = {
            "Name": name,
            "Gender_clean": gender,
            "Document_type_clean": doc_type,
            "Address_clean": address,
            "Document_Number": doc_number,
            "Combined_Data": data,
            "Fraud_Risk_Score": rule_score
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()

            prob = result["fraud_probability"]
            decision = result["decision"]

            st.subheader("Fraud Prediction Result")
            st.metric("Fraud Probability", f"{prob:.2f}")
            st.metric("Decision", decision)

            if prob > 0.85:
                st.error("⚠️ HIGH FRAUD RISK — BLOCK IMMEDIATELY")
            elif prob > 0.60:
                st.warning("⚠️ MEDIUM RISK — MANUAL REVIEW REQUIRED")
            else:
                st.success("✅ LOW RISK — PROCEED")

# ============================
# ✅ TAB 2 — FRAUD ANALYTICS
# ============================
with tab2:
    st.header("Fraud Risk Analytics Dashboard")

    df = pd.read_csv("data/raw_data.csv")
    df2 = pd.read_csv("model/output_of_GNN_part2.csv")


    show_stats_cards(df2)
    show_fraud_table(df2)

    fig = px.histogram(df2, x="GNN_Fraud_Probability", nbins=40, title="Fraud Probability Distribution")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(df2, x="Fraud_Risk_Score", y="GNN_Fraud_Probability",
                      color="Fraud_Risk_Level",
                      title="Rule Score vs GNN Prediction")
    st.plotly_chart(fig2, use_container_width=True)

# ============================
# ✅ TAB 3 — NETWORK GRAPH
# ============================
with tab3:
    st.header("KYC Similarity Network Graph")

    show_risk_graph(df2)
