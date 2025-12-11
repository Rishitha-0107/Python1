import json
from pathlib import Path
from typing import List
import pandas as pd
from datetime import datetime
# --- Configuration ---
RAW_DIR = Path("data/raw")
STAGED_DIR = Path("data/staged")
STAGED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = STAGED_DIR / "air_quality_transformed.csv"

POLLUTANTS = [
    "pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone", "uv_index"
]
# --- Helper functions ---
def categorize_aqi(pm2_5: float) -> str:
    if pm2_5 <= 50:
        return "Good"
    elif pm2_5 <= 100:
        return "Moderate"
    elif pm2_5 <= 200:
        return "Unhealthy"
    elif pm2_5 <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"
def compute_severity(row: pd.Series) -> float:
    return (
        row.get("pm2_5", 0) * 5 +
        row.get("pm10", 0) * 3 +
        row.get("nitrogen_dioxide", 0) * 4 +
        row.get("sulphur_dioxide", 0) * 4 +
        row.get("carbon_monoxide", 0) * 2 +
        row.get("ozone", 0) * 3
    )
def classify_risk(severity: float) -> str:
    if severity > 400:
        return "High Risk"
    elif severity > 200:
        return "Moderate Risk"
    else:
        return "Low Risk"
# --- Main transformation function ---
def transform_air_quality(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    all_records: List[pd.DataFrame] = []
    raw_files = sorted(raw_dir.glob("*_raw_*.json"))
    for file in raw_files:
        city_name = file.stem.split("_raw_")[0].replace("_", " ").title()
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Failed to read {file}: {e}")
            continue
        hourly_data = data.get("hourly", {})
        if not hourly_data:
            hourly_data = data.get("hourly", {})
        if "time" not in hourly_data:
            print(f"⚠️ No hourly time data found in {file}")
            continue
        n_records = len(hourly_data["time"])
        df_city = pd.DataFrame({"time": hourly_data["time"]})
        df_city["city"] = city_name
        for pollutant in POLLUTANTS:
            df_city[pollutant] = pd.to_numeric(hourly_data.get(pollutant, [None]*n_records), errors="coerce")
        df_city.dropna(subset=POLLUTANTS, how="all", inplace=True)
        df_city["time"] = pd.to_datetime(df_city["time"])
        # Derived features
        df_city["hour"] = df_city["time"].dt.hour
        df_city["AQI_Category"] = df_city["pm2_5"].apply(categorize_aqi)
        df_city["Severity_Score"] = df_city.apply(compute_severity, axis=1)
        df_city["Risk_Level"] = df_city["Severity_Score"].apply(classify_risk)
        all_records.append(df_city)
    if all_records:
        df_all = pd.concat(all_records, ignore_index=True)
        df_all.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Transformed data saved to {OUTPUT_FILE}")
        return df_all
    else:
        print("❌ No data transformed. Check raw files.")
        return pd.DataFrame()
# --- CLI Execution ---
if __name__ == "__main__":
    print("Starting transformation step...")
    df = transform_air_quality()
    print(f"Transformation complete. Rows: {len(df)}")
