import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="HR Attrition Dashboard",
    layout="wide"
)

st.title("HR Attrition Intelligence Platform")
st.caption("AI-powered Employee Retention & Risk Analytics")


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    r"employee_attrition_prediction_output.csv"
)

# ==========================================
# KPI METRICS
# ==========================================

total_employees = len(df)

high_risk_employees = len(
    df[df["attrition_probability"] >= 0.60]
)

avg_probability = round(
    df["attrition_probability"].mean(),
    2
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Employees", total_employees)

with col2:
    st.metric("High Risk Employees", high_risk_employees)

with col3:
    st.metric("Avg Attrition Probability", avg_probability)

with col4:
    st.metric(
        "Attrition Rate (%)",
        round(df["attrition_flag"].mean() * 100, 2)
    )

# ==========================================
# RISK CATEGORY DISTRIBUTION
# ==========================================

st.subheader("Risk Category Distribution")

st.bar_chart(df["ml_risk_category"].value_counts())

# ==========================================
# TOP 10 HIGH RISK EMPLOYEES
# ==========================================

st.subheader("Top 10 High Risk Employees")

top_10 = df.sort_values(
    by="attrition_probability",
    ascending=False
).head(10)

st.dataframe(
    top_10[
        [
            "employee_id",
            "attrition_probability",
            "top_risk_driver",
            "hr_recommendation"
        ]
    ]
)
st.subheader("Manager-wise Attrition Risk Ranking")

manager_risk = df.groupby("manager_id")["attrition_probability"].mean().sort_values(ascending=False).head(10)

st.bar_chart(manager_risk)

st.dataframe(manager_risk.reset_index().rename(
    columns={"attrition_probability": "avg_attrition_risk"}
))
st.subheader("Cost of Attrition (Estimated ₹ Impact)")

# assume avg cost = 30% of annual salary loss proxy
avg_salary = df["avg_base_salary"].mean()

attrition_count = len(df[df["attrition_flag"] == 1])

cost_per_employee = avg_salary * 0.30

total_cost = attrition_count * cost_per_employee

st.metric(
    "Estimated Attrition Cost (₹)",
    f"{round(total_cost/100000, 2)} Lakhs"
)

selected_emp = st.selectbox(
    "Select Employee ID for Deep Dive",
    df["employee_id"].unique()
)

st.write(df[df["employee_id"] == selected_emp])
st.subheader("💰 HR Budget Impact Analysis (Attrition Cost)")

# -----------------------------
# ASSUMPTIONS (can tune later)
# -----------------------------

avg_base_salary = df["avg_base_salary"].mean()

attrition_rate = df["attrition_flag"].mean()

total_employees = len(df)

# Estimated cost factors
replacement_cost_factor = 0.30   # 30% of salary
lost_productivity_factor = 0.20   # 20% productivity loss

# -----------------------------
# CALCULATIONS
# -----------------------------

avg_attrition_cost_per_employee = avg_base_salary * (
    replacement_cost_factor + lost_productivity_factor
)

total_attrition_cost = avg_attrition_cost_per_employee * (
    df["attrition_flag"].sum()
)

annual_hr_budget_impact = total_attrition_cost

# -----------------------------
# DISPLAY METRICS
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Avg Cost per Attrition (₹)",
        round(avg_attrition_cost_per_employee, 2)
    )

with col2:
    st.metric(
        "Total Attrition Cases",
        int(df["attrition_flag"].sum())
    )

with col3:
    st.metric(
        "Estimated HR Loss (₹)",
        f"{round(annual_hr_budget_impact/100000, 2)} Lakhs"
    )
    st.subheader("💰 Attrition Cost Breakdown (Finance View)")

# Assumptions
replacement_cost_pct = 0.30
productivity_loss_pct = 0.20
training_replacement_pct = 0.10

avg_salary = df["avg_base_salary"].mean()

total_attrition = df["attrition_flag"].sum()

# Costs
replacement_cost = avg_salary * replacement_cost_pct * total_attrition
productivity_loss = avg_salary * productivity_loss_pct * total_attrition
training_cost = avg_salary * training_replacement_pct * total_attrition

# DataFrame
cost_df = pd.DataFrame({
    "Cost Component": [
        "Replacement Cost",
        "Productivity Loss",
        "Training & Onboarding"
    ],
    "Cost (₹)": [
        replacement_cost,
        productivity_loss,
        training_cost
    ]
})

st.dataframe(cost_df.style.format({"Cost (₹)": "₹{:,.0f}"}))
st.subheader("Total Financial Impact")

total_cost = replacement_cost + productivity_loss + training_cost

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Attrition Cost", f"₹ {total_cost:,.0f}")

with col2:
    st.metric("Avg Cost per Employee", f"₹ {(total_cost/total_attrition):,.0f}")

with col3:
    st.metric("High Risk Exposure", f"{len(df[df['attrition_probability']>=0.6])} Employees")
    st.subheader("📈 Monthly Attrition Cost Trend")

df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")

df["month"] = df["hire_date"].dt.to_period("M")

monthly_cost = df.groupby("month")["attrition_flag"].sum() * df["avg_base_salary"].mean()

monthly_cost = monthly_cost.sort_index()

st.line_chart(monthly_cost)
st.subheader("🏢 Department-wise Attrition Cost Impact")

dept_cost = df.groupby("department_id").apply(
    lambda x: x["attrition_flag"].sum() * x["avg_base_salary"].mean()
)

st.bar_chart(dept_cost)
st.subheader("🎯 Attrition Reduction Scenario Simulator")

reduction_pct = st.slider(
    "Attrition Reduction Target (%)",
    0, 50, 10
)

current_cost = df["attrition_flag"].sum() * df["avg_base_salary"].mean()

future_cost = current_cost * (1 - reduction_pct / 100)

savings = current_cost - future_cost

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Cost", f"₹ {current_cost:,.0f}")

with col2:
    st.metric("Projected Cost", f"₹ {future_cost:,.0f}")

with col3:
    st.metric("Savings", f"₹ {savings:,.0f}")
    st.subheader("🤖 HR AI Assistant (Insights Generator)")

user_query = st.text_input("Ask something like: 'Why is attrition high?' or 'Which department is risky?'")

if user_query:

    if "department" in user_query.lower():
        risky_dept = df.groupby("department_id")["attrition_probability"].mean().idxmax()
        st.info(f"Highest risk department: {risky_dept}")

    elif "cost" in user_query.lower():
        total_cost = df["attrition_flag"].sum() * df["avg_base_salary"].mean()
        st.info(f"Estimated attrition cost: ₹ {total_cost:,.0f}")

    elif "risk" in user_query.lower():
        st.info("Top risk driver is typically Compensation and Experience factors based on SHAP analysis.")

    else:
        st.warning("Try asking about cost, risk, department, or attrition.")
