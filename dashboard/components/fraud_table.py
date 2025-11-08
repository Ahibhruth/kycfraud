import streamlit as st

def show_fraud_table(df):
    st.subheader("Top Suspicious Records")
    st.dataframe(df.sort_values("GNN_Fraud_Probability", ascending=False).head(20))
