import streamlit as st

def show_stats_cards(df):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Records", len(df))

    with col2:
        st.metric("High-Risk Records", (df["GNN_Fraud_Probability"] > 0.75).sum())

    with col3:
        st.metric("Average Fraud Probability", f"{df['GNN_Fraud_Probability'].mean():.2f}")
