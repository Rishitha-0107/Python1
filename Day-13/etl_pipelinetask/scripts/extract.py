import os
import pandas as pd

RAW_PATH = "data/raw"
os.makedirs(RAW_PATH, exist_ok=True)

url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"

df = pd.read_csv(url)
df.to_csv(f"{RAW_PATH}/churn_raw.csv", index=False)

print("Downloaded and saved churn_raw.csv successfully!")
