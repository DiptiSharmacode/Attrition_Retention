import streamlit as st
import pandas as pd

st.set_page_config(
page_title="HR Attrition Analytics",
layout="wide"
)

st.title("HR Attrition & Retention Analytics Dashboard")

df = pd.read_csv(
r"employee_attrition_prediction_output.csv"
)

st.subheader("Dataset Overview")

st.write(df.head())

st.metric(
"Total Employees",
len(df)
)

st.metric(
"High Risk Employees",
len(df[df['attrition_probability'] >= 0.60])
)

st.subheader("Risk Distribution")

st.bar_chart(
df['ml_risk_category'].value_counts()
)

st.subheader("Employee Search")

employee_id = st.selectbox(
"Select Employee",
sorted(df['employee_id'].unique())
)

employee = df[df['employee_id'] == employee_id]

st.dataframe(employee)
st.sidebar.success("Select a page above to explore HR insights")
