import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# -----------------------------
# 1️⃣ App Header
# -----------------------------
st.title("💳Customer Risk Prediction System (KNN)")
st.write(
    "This system predicts customer risk by comparing them with similar customers."
)

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("credit_risk_dataset.csv")
    return df

df = load_data()

# -----------------------------
# Basic Preprocessing
# -----------------------------
df['person_emp_length'].fillna(df['person_emp_length'].median(), inplace=True)
df['loan_int_rate'].fillna(df['loan_int_rate'].median(), inplace=True)

# Binary encode credit history
df['cb_person_default_on_file'] = df['cb_person_default_on_file'].map({'Y': 1, 'N': 0})

# Select required features only (simple & exam-friendly)
features = [
    'person_age',
    'person_income',
    'loan_amnt',
    'cb_person_default_on_file'
]

X = df[features]
y = df['loan_status']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# 2️⃣ Sidebar – User Inputs
# -----------------------------
st.sidebar.header("Enter Customer Details")

age = st.sidebar.slider("Age", 18, 70, 25)
income = st.sidebar.number_input("Annual Income", 10000, 10000000, 500000)
loan_amount = st.sidebar.number_input("Loan Amount", 1000, 1000000, 200000)
credit_history = st.sidebar.radio("Credit History", ["Yes", "No"])

# 🔥 Important KNN Concept
k_value = st.sidebar.slider("K Value (Number of Neighbors)", 1, 15, 5)

credit_history_val = 0 if credit_history == "Yes" else 1

# -----------------------------
# Prepare Input
# -----------------------------
input_data = np.array([[age, income, loan_amount, credit_history_val]])
input_scaled = scaler.transform(input_data)

# -----------------------------
# Train KNN Model
# -----------------------------
knn = KNeighborsClassifier(n_neighbors=k_value)
knn.fit(X_scaled, y)

# -----------------------------
# 3️⃣ Prediction Button
# -----------------------------
if st.button("Predict Customer Risk"):

    prediction = knn.predict(input_scaled)[0]
    distances, indices = knn.kneighbors(input_scaled)

    neighbor_classes = y.iloc[indices[0]]
    majority_class = neighbor_classes.mode()[0]

    # -----------------------------
    # 4️⃣ Prediction Output
    # -----------------------------
    if prediction == 1:
        st.markdown(
            "<h2 style='color:red; text-align:center;'>🔴 High Risk Customer</h2>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<h2 style='color:green; text-align:center;'>🟢 Low Risk Customer</h2>",
            unsafe_allow_html=True
        )

    # -----------------------------
    # 5️⃣ Nearest Neighbors Explanation
    # -----------------------------
    st.subheader("Nearest Neighbors Explanation")

    st.write(f"**Number of neighbors considered (K):** {k_value}")
    st.write(
        f"**Majority class among neighbors:** "
        f"{'High Risk' if majority_class == 1 else 'Low Risk'}"
    )

    neighbors_df = df.iloc[indices[0]][features + ['loan_status']]
    neighbors_df['loan_status'] = neighbors_df['loan_status'].map(
        {1: 'High Risk', 0: 'Low Risk'}
    )

    st.write("Nearest Customers Used for Decision:")
    st.dataframe(neighbors_df)

    # -----------------------------
    # 6️⃣ Business Insight Section
    # -----------------------------
    st.subheader("Business Insight")
    st.info(
        "This decision is based on similarity with nearby customers in feature space. "
        "The KNN algorithm compares the customer with similar past cases and assigns "
        "the risk based on the majority behavior of those neighbors."
    )
