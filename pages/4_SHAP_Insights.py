import streamlit as st
import pandas as pd

st.title("SHAP Insights")

shap_df = pd.read_csv(
    r"shap_feature_importance.csv"
)

st.dataframe(shap_df.head(15))

st.bar_chart(
    shap_df.head(10).set_index('feature')
)
st.title("HR Attrition Intelligence Platform")
st.caption("AI-powered Employee Retention & Risk Analytics")
