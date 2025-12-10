import os
import pandas as pd

def generate_summary(input_path, output_path):
    print("📊 Generating analytics summary...")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"❌ File not found: {input_path}")

    df = pd.read_csv(input_path)

    summary_rows = []
    # 1️⃣ Overall Churn Rate
    churn_rate = df["Churn"].value_counts(normalize=True) * 100
    summary_rows.append(["Overall Churn Rate (%)", churn_rate.get("Yes", 0)])
    # 2️⃣ Churn by Contract Type
    churn_contract = df.groupby("Contract")["Churn"].value_counts(normalize=True).unstack().fillna(0) * 100
    summary_rows.append(["Churn - Month-to-month (%)", churn_contract.loc["Month-to-month"].get("Yes", 0) if "Month-to-month" in churn_contract.index else 0])
    summary_rows.append(["Churn - One year (%)", churn_contract.loc["One year"].get("Yes", 0) if "One year" in churn_contract.index else 0])
    summary_rows.append(["Churn - Two year (%)", churn_contract.loc["Two year"].get("Yes", 0) if "Two year" in churn_contract.index else 0])
    # 3️⃣ Churn by Internet Service
    churn_internet = df.groupby("InternetService")["Churn"].value_counts(normalize=True).unstack().fillna(0) * 100
    for service in churn_internet.index:
        summary_rows.append([f"Churn - {service} (%)", churn_internet.loc[service].get("Yes", 0)])
    # 4️⃣ Churn by Tenure Group
    if "tenure_group" in df.columns:
        churn_tenure = df.groupby("tenure_group")["Churn"].value_counts(normalize=True).unstack().fillna(0) * 100
        for group in churn_tenure.index:
            summary_rows.append([f"Churn - Tenure: {group} (%)", churn_tenure.loc[group].get("Yes", 0)])
    # 5️⃣ Monthly Charges Segment
    if "monthly_charge_segment" in df.columns:
        churn_charge = df.groupby("monthly_charge_segment")["Churn"].value_counts(normalize=True).unstack().fillna(0) * 100
        for seg in churn_charge.index:
            summary_rows.append([f"Churn - Charges {seg} (%)", churn_charge.loc[seg].get("Yes", 0)])
    # Save results
    summary_df = pd.DataFrame(summary_rows, columns=["Metric", "Value"])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    summary_df.to_csv(output_path, index=False)
    print("✅ Summary generated!")
    print(f"📄 Saved to: {output_path}")
    return summary_df
if __name__ == "__main__":
    input_file = "data/processed/churn_final.csv"
    output_file = "data/processed/analytics_summary.csv"
    generate_summary(input_file, output_file)
