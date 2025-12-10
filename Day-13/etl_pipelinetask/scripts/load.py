import os
import pandas as pd

def load_processed_data(input_path, output_path):
    print("📥Loading transformed dataset...")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"❌ Transformed file not found: {input_path}")
    df = pd.read_csv(input_path)
    print("🧹 Final formatting...")
    df.columns = [col.strip().replace(" ", "_") for col in df.columns]
    # Create processed folder if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print("✅Load complete!")
    print(f"📁Final dataset saved to: {output_path}")
    return df
if __name__ == "__main__":
    input_file="data/staged/churn_transformed.csv"
    output_file="data/processed/churn_final.csv"
    load_processed_data(input_file, output_file)
