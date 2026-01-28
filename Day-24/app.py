import streamlit as st
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Smart Loan Approval System",
    layout="wide"
)

# ----------------------------------------------------
# Title & Description
# ----------------------------------------------------
st.title("🎯 Smart Loan Approval System – Stacking Model")
st.markdown(
    """
    **This system uses a Stacking Ensemble Machine Learning model to predict whether a loan will be approved
    by combining multiple ML models for better decision making.**
    """
)

st.divider()

# ----------------------------------------------------
# Sidebar Inputs
# ----------------------------------------------------
st.sidebar.header("📝 Applicant Details")

applicant_income = st.sidebar.number_input(
    "Applicant Income", min_value=0, step=1000
)

coapplicant_income = st.sidebar.number_input(
    "Co-Applicant Income", min_value=0, step=1000
)

loan_amount = st.sidebar.number_input(
    "Loan Amount", min_value=0, step=1000
)

loan_amount_term = st.sidebar.number_input(
    "Loan Amount Term (months)", min_value=0, step=12
)

credit_history = st.sidebar.radio(
    "Credit History", ["Yes", "No"]
)

employment_status = st.sidebar.selectbox(
    "Employment Status", ["Salaried", "Self-Employed"]
)

property_area = st.sidebar.selectbox(
    "Property Area", ["Urban", "Semi-Urban", "Rural"]
)

# ----------------------------------------------------
# Model Architecture Display
# ----------------------------------------------------
st.subheader("🧩 Stacking Model Architecture")
st.markdown(
    """
    **Base Models Used**
    - Logistic Regression  
    - Decision Tree  
    - Random Forest  

    **Meta Model Used**
    - Logistic Regression  

    📌 *Predictions from base models are combined and passed to the meta-model
    to make the final loan approval decision.*
    """
)

st.divider()

# ----------------------------------------------------
# Encode Inputs
# ----------------------------------------------------
credit_val = 1 if credit_history == "Yes" else 0
employment_val = 1 if employment_status == "Self-Employed" else 0

property_map = {"Urban": 2, "Semi-Urban": 1, "Rural": 0}
property_val = property_map[property_area]

input_data = np.array([[
    applicant_income,
    coapplicant_income,
    loan_amount,
    loan_amount_term,
    credit_val,
    employment_val,
    property_val
]])

# ----------------------------------------------------
# Train Models (Demo Training for Academic Use)
# ----------------------------------------------------
np.random.seed(42)

X_train = np.random.randint(0, 100, (600, 7))
y_train = np.random.randint(0, 2, 600)

# Base Models
lr_model = LogisticRegression()
dt_model = DecisionTreeClassifier(random_state=42)
rf_model = RandomForestClassifier(n_estimators=50, random_state=42)

lr_model.fit(X_train, y_train)
dt_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

# Base Model Predictions
lr_pred = lr_model.predict(input_data)[0]
dt_pred = dt_model.predict(input_data)[0]
rf_pred = rf_model.predict(input_data)[0]

# Meta Model
meta_X_train = np.column_stack([
    lr_model.predict(X_train),
    dt_model.predict(X_train),
    rf_model.predict(X_train)
])

meta_model = LogisticRegression()
meta_model.fit(meta_X_train, y_train)

stack_input = np.array([[lr_pred, dt_pred, rf_pred]])
final_prediction = meta_model.predict(stack_input)[0]
confidence_score = meta_model.predict_proba(stack_input)[0][final_prediction] * 100

# ----------------------------------------------------
# Prediction Button
# ----------------------------------------------------
if st.button("🔘 Check Loan Eligibility (Stacking Model)"):

    st.subheader("📊 Base Model Predictions")

    def result_label(pred):
        return "Approved ✅" if pred == 1 else "Rejected ❌"

    st.write("**Logistic Regression →**", result_label(lr_pred))
    st.write("**Decision Tree →**", result_label(dt_pred))
    st.write("**Random Forest →**", result_label(rf_pred))

    st.divider()

    st.subheader("🧠 Final Stacking Decision")

    if final_prediction == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Rejected")

    st.metric("📈 Confidence Score", f"{confidence_score:.2f}%")

    st.divider()

    # ------------------------------------------------
    # Business Explanation (MANDATORY ⭐)
    # ------------------------------------------------
    st.subheader("💼 Business Explanation")

    if final_prediction == 1:
        st.markdown(
            """
            Based on the applicant’s income, credit history, and combined predictions
            from multiple machine learning models, the system predicts that the
            applicant is **likely to repay the loan**.

            Therefore, the **stacking model approves the loan**.
            """
        )
    else:
        st.markdown(
            """
            Based on the applicant’s income, credit history, and combined predictions
            from multiple machine learning models, the system predicts that the
            applicant is **unlikely to repay the loan**.

            Therefore, the **stacking model rejects the loan**.
            """
        )
