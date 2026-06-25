import streamlit as st
import pandas as pd

# ==========================================
# PAGE TITLE
# ==========================================

st.title("🚨 High Risk Employees Dashboard")

st.caption("AI-driven HR intervention list for retention actions")

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    r"employee_attrition_prediction_output.csv"
)

df.columns = df.columns.str.strip()

# ==========================================
# HIGH RISK FILTER
# ==========================================

high_risk_df = df[df["attrition_probability"] >= 0.60]

# ==========================================
# KPI CARDS
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Employees", len(df))

with col2:
    st.metric("High Risk Employees", len(high_risk_df))

with col3:
    st.metric("High Risk %", round(len(high_risk_df) / len(df) * 100, 2))

# ==========================================
# DEPARTMENT WISE RISK INSIGHT
# ==========================================

st.subheader("Department-wise High Risk Distribution")

dept_risk = high_risk_df["department_id"].value_counts()

st.bar_chart(dept_risk)

# ==========================================
# TOP HIGH RISK EMPLOYEES
# ==========================================

st.subheader("Top 15 High Risk Employees")

top_risk = high_risk_df.sort_values(
    by="attrition_probability",
    ascending=False
).head(15)

st.dataframe(
    top_risk[
        [
            "employee_id",
            "department_id",
            "attrition_probability",
            "ml_risk_category",
            "top_risk_driver",
            "hr_recommendation"
        ]
    ]
)

# ==========================================
# ==========================================
# HR ACTION SUMMARY (BEST PRACTICE VERSION)
# ==========================================

st.subheader("HR Action Summary")

if len(high_risk_df) > 0:

    # Ensure numeric safety
    risk_cols = [
        "comp_risk",
        "productivity_risk",
        "performance_risk",
        "development_risk",
        "career_risk",
        "experience_risk"
    ]

    # Convert safely (VERY IMPORTANT)
    high_risk_df[risk_cols] = high_risk_df[risk_cols].apply(
        pd.to_numeric, errors="coerce"
    ).fillna(0)

    # Compute MEAN risk impact (real analytics approach)
    risk_summary = high_risk_df[risk_cols].mean().sort_values(ascending=False)

    # Display KPI-style summary
    st.write("### 🔍 Risk Category Impact (Average Scores)")

    for risk_name, value in risk_summary.items():
        st.write(f"• {risk_name.replace('_', ' ').title()}: {round(value, 2)}")

    # Identify TOP risk driver
    top_risk_driver = risk_summary.index[0].replace("_", " ").title()

    st.markdown("---")

    st.write("### 🎯 HR Priority Recommendation")

    st.warning(f"""
    👉 Highest Risk Driver: **{top_risk_driver}**

    HR should prioritize interventions in this area first.

    Suggested Actions:
    """)

    # Action mapping (PROFESSIONAL HR LOGIC)
    action_map = {
        "Comp Risk": "Conduct salary benchmarking, review compensation fairness, adjust pay bands.",
        "Productivity Risk": "Review workload distribution and overtime patterns.",
        "Performance Risk": "Initiate performance coaching and manager feedback sessions.",
        "Development Risk": "Provide targeted training and skill development programs.",
        "Career Risk": "Enable internal mobility and career progression discussions.",
        "Experience Risk": "Improve employee engagement and HR support responsiveness."
    }

    for key, action in action_map.items():
        if key in top_risk_driver:
            st.info(action)

else:
    st.warning("No high risk employees found.")
# ==========================================
# DOWNLOAD REPORT
# ==========================================

csv = high_risk_df.to_csv(index=False)

st.download_button(
    label="⬇ Download High Risk Employee Report",
    data=csv,
    file_name="high_risk_employees_report.csv",
    mime="text/csv"
)
st.write(high_risk_df["top_risk_driver"].value_counts())
st.subheader("HR Email Alert Simulation")

critical_employees = df[df["attrition_probability"] >= 0.75]

if len(critical_employees) > 0:

    for _, row in critical_employees.head(5).iterrows():

        st.error(f"""
        📧 HR ALERT EMAIL

        To: hr@company.com  
        Subject: High Attrition Risk Alert - Employee {row['employee_id']}

        Message:
        Employee {row['employee_id']} has a HIGH attrition risk of {round(row['attrition_probability'],2)}.

        Risk Driver: {row['top_risk_driver']}

        Recommended Action:
        {row['hr_recommendation']}
        """)
else:
    st.success("No critical employees requiring email alerts.")
