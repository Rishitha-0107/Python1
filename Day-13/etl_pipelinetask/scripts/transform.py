import os
import pandas as pd

def transform_churn_data(input_path, output_path):
    print("🔄Transforming dataset.....")
    df=pd.read_csv(input_path)
    # 1. Convert TotalCharges to numeric
    df["TotalCharges"]=pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"]=df["TotalCharges"].fillna(df["TotalCharges"].median())
    # 2. Replace "No internet service" and "No phone service"
    replace_cols=[
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
        'StreamingTV', 'StreamingMovies', 'MultipleLines'
    ]
    for col in replace_cols:
        if col in df.columns:
            df[col]=df[col].replace({'No internet service': 'No', 'No phone service': 'No'})
    # 3. Encode binary Yes/No columns
    binary_cols=[col for col in df.columns if df[col].isin(['Yes', 'No']).all()]
    for col in binary_cols:
        df[col]=df[col].map({'Yes': 1,'No': 0})
    # 4. Save transformed file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print("✅Transformation complete!")
    print("📤Saved to:",output_path)
    return df
if __name__ == "__main__":
    input_file="data/raw/churn_raw.csv"
    output_file="data/staged/churn_transformed.csv"
    transform_churn_data(input_file, output_file)
