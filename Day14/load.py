
import os
import time
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import math

from supabase import create_client, Client

# Load env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = os.getenv("SUPABASE_TABLE", "aqd1")
STAGED_CSV = os.getenv("STAGED_CSV", "data/staged/air_quality_transformed.csv")

BATCH_SIZE = int(os.getenv("LOAD_BATCH_SIZE", 200))
MAX_RETRIES = int(os.getenv("LOAD_MAX_RETRIES", 2))  # number of retries after first attempt
RETRY_DELAY = float(os.getenv("LOAD_RETRY_DELAY", 2.0))  # seconds

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # lower-case columns for consistency
    df.columns = [c.lower() for c in df.columns]

    # mapping: transform used 'aqi_category', 'severity_score', 'risk_level', 'hour_of_day'
    if "risk_level" in df.columns and "risk_flag" not in df.columns:
        df["risk_flag"] = df["risk_level"]
    if "hour_of_day" in df.columns and "hour" not in df.columns:
        df["hour"] = df["hour_of_day"]
    # Ensure required columns exist (fill missing with None)
    required = [
        "city", "time", "pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide",
        "sulphur_dioxide", "ozone", "uv_index", "aqi_category",
        "severity_score", "risk_flag", "hour"
    ]
    for col in required:
        if col not in df.columns:
            df[col] = None
    # Convert time -> datetime
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    # Ensure numeric columns are numeric
    numerics = ["pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide",
                "sulphur_dioxide", "ozone", "uv_index", "severity_score"]
    for n in numerics:
        df[n] = pd.to_numeric(df[n], errors="coerce")
    # Ensure hour is integer (nullable)
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce").astype('Int64')
    return df[required]
def _row_to_record(row: pd.Series) -> dict:
    record = {}
    for k, v in row.items():
        # handle pandas NA
        if pd.isna(v):
            record[k] = None
            continue
        # datetimes
        if hasattr(v, "isoformat"):
            try:
                record[k] = v.isoformat()
                continue
            except Exception:
                pass
        # numpy types
        if isinstance(v, (np.floating, float)):
            if math.isnan(v):
                record[k] = None
            else:
                record[k] = float(v)
            continue
        if isinstance(v, (np.integer, int)):
            record[k] = int(v)
            continue
        record[k] = v
    return record
def load_to_supabase(df: pd.DataFrame):
    df_norm = _normalize_df(df)
    rows = df_norm.to_dict(orient="records")
    total = len(rows)
    inserted = 0
    failed_batches = 0
    for start in range(0, total, BATCH_SIZE):
        batch = rows[start:start + BATCH_SIZE]
        attempt = 0
        success = False
        while attempt <= MAX_RETRIES and not success:
            try:
                cleaned = [_row_to_record(pd.Series(b)) for b in batch]
                res = supabase.table(TABLE_NAME).insert(cleaned).execute()
                # supabase client returns different shapes; treat lack of exception as success
                success = True
                inserted += len(batch)
                print(f"Inserted batch {start//BATCH_SIZE + 1}: rows {start+1}-{start+len(batch)}")
            except Exception as e:
                attempt += 1
                print(f"❌ Batch {start//BATCH_SIZE + 1} failed (attempt {attempt}): {e}")
                if attempt <= MAX_RETRIES:
                    print(f"⏳ Retrying in {RETRY_DELAY}s...")
                    time.sleep(RETRY_DELAY)
                else:
                    print("❌ Max retries reached for this batch.")
                    failed_batches += 1
        # end batch loop
    print("========================================")
    print(f"Total rows processed: {total}")
    print(f"Total rows inserted:  {inserted}")
    if failed_batches:
        print(f"Batches failed:       {failed_batches}")
    else:
        print("All batches inserted successfully.")
    print("========================================")
    return {"total": total, "inserted": inserted, "failed_batches": failed_batches}
if __name__ == "__main__":
    if not os.path.exists(STAGED_CSV):
        raise FileNotFoundError(f"Staged CSV not found at: {STAGED_CSV}. Run transform.py first.")
    df = pd.read_csv(STAGED_CSV)
    load_to_supabase(df)