import os
import pandas as pd

def validate_data(input_path, report_path):
    print("🔍Running dataset validation checks...")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"❌File not found: {input_path}")
    df = pd.read_csv(input_path)
    report_lines = []
    # 1. Basic info
    report_lines.append("===== DATA VALIDATION REPORT =====\n")
    report_lines.append(f"Rows: {df.shape[0]}")
    report_lines.append(f"Columns: {df.shape[1]}\n")
    # 2. Missing values
    missing = df.isnull().sum()
    report_lines.append("🔸Missing Values:\n")
    report_lines.append(str(missing))
    report_lines.append("\n")
    # 3. Duplicate records
    duplicates = df.duplicated().sum()
    report_lines.append(f"🔸Duplicate Rows: {duplicates}\n")
    # 4. Datatype summary
    report_lines.append("🔸Datatypes:\n")
    report_lines.append(str(df.dtypes))
    report_lines.append("\n")
    # 5. Check expected columns
    required_cols = ["tenure", "MonthlyCharges", "TotalCharges", "Churn"]
    report_lines.append("Required Columns Check:\n")
    for col in required_cols:
        if col in df.columns:
            report_lines.append(f"{col} — OK")
        else:
            report_lines.append(f"{col} — MISSING")
    report_lines.append("\n")

   
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print("📄Validation complete!")
    print(f"📁Report saved to: {report_path}")
if __name__ == "__main__":
    input_file = "data/processed/churn_final.csv"
    report_file = "data/processed/validation_report.txt"

    validate_data(input_file, report_file)
