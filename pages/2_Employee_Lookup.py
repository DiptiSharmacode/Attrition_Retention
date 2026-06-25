import streamlit as st
import pandas as pd

# ==========================================
# PAGE TITLE
# ==========================================

st.title("Employee Attrition Lookup")

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    r"employee_attrition_prediction_output.csv"
)

# ==========================================
# EMPLOYEE SELECTION
# ==========================================

employee_id = st.selectbox(
    "Select Employee ID",
    sorted(df["employee_id"].unique())
)

employee = df[
    df["employee_id"] == employee_id
]

# ==========================================
# EMPLOYEE RECORD
# ==========================================

st.subheader("Employee Record")

st.dataframe(employee)

# ==========================================
# ATTRITION DETAILS
# ==========================================

st.subheader("Attrition Risk Analysis")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Attrition Probability",
        round(
            float(employee["attrition_probability"].iloc[0]),
            2
        )
    )

with col2:
    st.metric(
        "Risk Category",
        str(employee["ml_risk_category"].iloc[0])
    )

# ==========================================
# TOP RISK DRIVER
# ==========================================

st.subheader("Top Risk Driver")

st.info(
    str(employee["top_risk_driver"].iloc[0])
)

# ==========================================
# HR RECOMMENDATION
# ==========================================

st.subheader("HR Recommendation")

st.success(
    str(employee["hr_recommendation"].iloc[0])
)

# ==========================================
# RISK BREAKDOWN
# ==========================================

st.subheader("Risk Breakdown")

risk_df = pd.DataFrame({
    "Risk Category": [
        "Compensation",
        "Productivity",
        "Performance",
        "Development",
        "Career",
        "Experience"
    ],
    "Risk Score": [
        employee["comp_risk"].iloc[0],
        employee["productivity_risk"].iloc[0],
        employee["performance_risk"].iloc[0],
        employee["development_risk"].iloc[0],
        employee["career_risk"].iloc[0],
        employee["experience_risk"].iloc[0]
    ]
})

st.bar_chart(
    risk_df.set_index("Risk Category")
)

# ==========================================
# TOP 3 RISK FACTORS
# ==========================================

st.subheader("Top 3 Risk Factors")

top_risks = risk_df.sort_values(
    by="Risk Score",
    ascending=False
).head(3)

st.dataframe(top_risks)

# ==========================================
# WHY THIS RECOMMENDATION
# ==========================================

st.subheader("Why This Recommendation?")

highest_risk = top_risks.iloc[0]["Risk Category"]

if highest_risk == "Compensation":

    st.warning("""
    This employee shows elevated compensation risk.

    Possible indicators:
    • Lower compensation competitiveness
    • Bonus-related concerns
    • Compensation growth stagnation

    Recommended action:
    Salary benchmarking and compensation review.
    """)

elif highest_risk == "Development":

    st.warning("""
    This employee shows elevated development risk.

    Possible indicators:
    • Limited training participation
    • Lower certification attainment
    • Reduced learning activity

    Recommended action:
    Create a personalized learning plan.
    """)

elif highest_risk == "Career":

    st.warning("""
    This employee shows elevated career risk.

    Possible indicators:
    • Promotion delays
    • Limited internal mobility

    Recommended action:
    Conduct career path discussion.
    """)

elif highest_risk == "Experience":

    st.warning("""
    This employee shows elevated employee experience risk.

    Possible indicators:
    • Grievances
    • HR ticket history
    • Workplace concerns

    Recommended action:
    HRBP intervention and employee listening session.
    """)

elif highest_risk == "Productivity":

    st.warning("""
    This employee shows elevated productivity risk.

    Possible indicators:
    • Overtime burden
    • Productivity fluctuations

    Recommended action:
    Review workload allocation.
    """)

elif highest_risk == "Performance":

    st.warning("""
    This employee shows elevated performance risk.

    Possible indicators:
    • Performance decline
    • KPI achievement gaps

    Recommended action:
    Manager coaching and development support.
    """)

# ==========================================
# MODEL EXPLAINABILITY
# ==========================================

st.subheader("Model Explainability")

st.info("""
The attrition model identified the following
key drivers of employee attrition:

• Base Salary
• Gross Pay
• Net Pay
• Bonus Amount
• Training Investment
• Certification Performance
• Grievance Resolution Time
• Overtime Hours
• Burnout Indicators

These drivers were identified using SHAP Explainability.
""")
st.title("HR Attrition Intelligence Platform")
st.caption("AI-powered Employee Retention & Risk Analytics")
risk = employee["ml_risk_category"].iloc[0]
st.subheader("Risk Category")

if risk == "Very High Risk":
    st.error(risk)
elif risk == "High Risk":
    st.warning(risk)
elif risk == "Medium Risk":
    st.info(risk)
else:
    st.success(risk)
# ==========================================
# TOP RISK DRIVER (ROBUST VERSION)
# ==========================================

risk_cols = [
    "comp_risk",
    "productivity_risk",
    "performance_risk",
    "development_risk",
    "career_risk",
    "experience_risk"
]

# ensure numeric + no NaN issues
employee_risks = employee[risk_cols].iloc[0].apply(pd.to_numeric, errors="coerce").fillna(0)

top_risk_col = employee_risks.idxmax()
top_risk_value = employee_risks.max()

# clean label for display
top_risk_driver = top_risk_col.replace("_", " ").title()

st.subheader("Top Risk Driver")

st.error(f"""
{top_risk_driver}

Score: {round(top_risk_value, 2)}
""")
from io import BytesIO

st.subheader("📄 Download Employee HR Report")

selected_emp = df.sample(1)

buffer = BytesIO()

report_text = f"""
Employee HR Report

Employee ID: {selected_emp['employee_id'].values[0]}
Attrition Probability: {selected_emp['attrition_probability'].values[0]}
Risk Category: {selected_emp['ml_risk_category'].values[0]}
Top Risk Driver: {selected_emp['top_risk_driver'].values[0]}
HR Recommendation: {selected_emp['hr_recommendation'].values[0]}
"""

st.download_button(
    label="Download HR Report",
    data=report_text,
    file_name="employee_hr_report.txt",
    mime="text/plain"
)



