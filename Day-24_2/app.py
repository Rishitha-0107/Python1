import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")

# --------------------------------------------------
# Title & Description
# --------------------------------------------------
st.title("🟢 Customer Segmentation Dashboard")
st.markdown(
    """
    **This system uses K-Means Clustering to group customers based on their purchasing
    behavior and similarities.**

    👉 *Discover hidden customer groups without predefined labels.*
    """
)

st.divider()

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = pd.read_csv("Wholesale customers data.csv")

# Only numerical columns
numerical_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

# --------------------------------------------------
# Sidebar – Input Section (Mandatory)
# --------------------------------------------------
st.sidebar.header("⚙️ Clustering Controls")

feature_1 = st.sidebar.selectbox(
    "Select Feature 1", numerical_cols, index=0
)

feature_2 = st.sidebar.selectbox(
    "Select Feature 2", numerical_cols, index=1
)

k = st.sidebar.slider(
    "Number of Clusters (K)", min_value=2, max_value=10, value=3
)

random_state = st.sidebar.number_input(
    "Random State (Optional)", value=42, step=1
)

run_button = st.sidebar.button("🟦 Run Clustering")

# --------------------------------------------------
# Validation: Minimum 2 Features
# --------------------------------------------------
if feature_1 == feature_2:
    st.warning("⚠️ Please select two different numerical features.")
    st.stop()

# --------------------------------------------------
# Main Logic – Run Clustering
# --------------------------------------------------
if run_button:

    st.header("📊 Clustering Results")

    X = df[[feature_1, feature_2]]

    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-Means Model
    kmeans = KMeans(n_clusters=k, random_state=random_state)
    clusters = kmeans.fit_predict(X_scaled)

    df["Cluster"] = clusters

    # --------------------------------------------------
    # Visualization Section
    # --------------------------------------------------
    st.subheader("🔹 Cluster Visualization")

    fig, ax = plt.subplots()

    scatter = ax.scatter(
        X_scaled[:, 0],
        X_scaled[:, 1],
        c=clusters,
        cmap="viridis",
        alpha=0.6
    )

    centers = kmeans.cluster_centers_
    ax.scatter(
        centers[:, 0],
        centers[:, 1],
        c="red",
        s=200,
        marker="X",
        label="Cluster Centers"
    )

    ax.set_xlabel(feature_1)
    ax.set_ylabel(feature_2)
    ax.set_title("Customer Clusters (K-Means)")
    ax.legend()

    st.pyplot(fig)

    # --------------------------------------------------
    # Cluster Summary Section
    # --------------------------------------------------
    st.subheader("📋 Cluster Summary")

    summary = (
        df.groupby("Cluster")[[feature_1, feature_2]]
        .agg(["mean", "count"])
        .round(2)
    )

    summary.columns = ["Avg " + feature_1, "Count",
                       "Avg " + feature_2, ""]

    summary = summary.drop(columns=[""])

    st.dataframe(summary)

    # --------------------------------------------------
    # Business Interpretation Section
    # --------------------------------------------------
    st.subheader("💼 Business Interpretation")

    for cluster_id in sorted(df["Cluster"].unique()):
        cluster_data = df[df["Cluster"] == cluster_id]
        avg_1 = cluster_data[feature_1].mean()
        avg_2 = cluster_data[feature_2].mean()

        if avg_1 > X[feature_1].mean() and avg_2 > X[feature_2].mean():
            insight = "High-spending customers across multiple categories"
            icon = "🟢"
        elif avg_1 < X[feature_1].mean() and avg_2 < X[feature_2].mean():
            insight = "Budget-conscious customers with lower spending"
            icon = "🟡"
        else:
            insight = "Moderate spenders with selective purchasing behavior"
            icon = "🔵"

        st.markdown(
            f"**{icon} Cluster {cluster_id}:** {insight}"
        )

    # --------------------------------------------------
    # User Guidance / Insight Box
    # --------------------------------------------------
    st.info(
        "Customers in the same cluster exhibit similar purchasing behaviour "
        "and can be targeted with similar business strategies."
    )

else:
    st.info("⬅️ Select features and click **Run Clustering** to view results.")
