# extract.py

"""
Extract step for AtmosTrack Air Quality ETL using Open-Meteo API.

- Fetches hourly pollutants including PM10, PM2.5, CO, NO2, O3, SO2, UV index.
- Implements retry with exponential backoff (default 3 attempts).
- Saves raw JSON responses to data/raw/<city>_raw_<timestamp>.json.
- Returns a list of dicts containing city and saved file paths.
"""

from __future__ import annotations
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
RAW_DIR = Path(os.getenv("RAW_DIR", Path(__file__).resolve().parents[0] / "data" / "raw"))
RAW_DIR.mkdir(parents=True, exist_ok=True)

API_BASE = os.getenv("AIR_METEO_API_BASE", "https://air-quality-api.open-meteo.com/v1/air-quality")
CITY_COORDS = os.getenv("CITY_COORDS", "").split(";")

MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "10"))
SLEEP_BETWEEN_CALLS = float(os.getenv("SLEEP_BETWEEN_CALLS", "0.5"))

# --- Helper functions ---
def _now_ts() -> str:
    """UTC timestamp for filenames."""
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

def _save_raw(payload: object, city: str) -> str:
    """Save JSON payload to RAW_DIR and return absolute path."""
    ts = _now_ts()
    filename = f"{city.replace(' ', '_').lower()}_raw_{ts}.json"
    path = RAW_DIR / filename
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    except Exception:
        path = RAW_DIR / f"{city.replace(' ', '_').lower()}_raw_{ts}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(repr(payload))
    return str(path.resolve())

def _fetch_city(city: str, lat: float, lon: float, max_retries: int = MAX_RETRIES, timeout: int = TIMEOUT_SECONDS) -> Dict[str, Optional[str]]:
    """
    Fetch air quality data for a city with retry logic.
    Returns dict: city, success, raw_path or error.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide,uv_index"
    }
    attempt = 0
    last_error: Optional[str] = None

    while attempt < max_retries:
        attempt += 1
        try:
            resp = requests.get(API_BASE, params=params, timeout=timeout)
            resp.raise_for_status()
            try:
                payload = resp.json()
            except ValueError:
                payload = {"raw_text": resp.text}

            saved = _save_raw(payload, city)
            print(f"✅ [{city}] fetched and saved to: {saved}")
            return {"city": city, "success": "true", "raw_path": saved}

        except requests.RequestException as e:
            last_error = str(e)
            print(f"⚠️ [{city}] attempt {attempt}/{max_retries} failed: {e}")
        except Exception as e:
            last_error = str(e)
            print(f"⚠️ [{city}] unexpected error on attempt {attempt}: {e}")

        backoff = 2 ** (attempt - 1)
        print(f"⏳ [{city}] retrying in {backoff}s ...")
        time.sleep(backoff)

    print(f"❌ [{city}] failed after {max_retries} attempts. Last error: {last_error}")
    return {"city": city, "success": "false", "error": last_error}

def fetch_all_cities(city_coords: Optional[List[str]] = None) -> List[Dict[str, Optional[str]]]:
    """
    Fetch AQ data for all cities (lat,lon pairs in CITY_COORDS)
    Returns list of dicts for each city.
    """
    if city_coords is None:
        city_coords = CITY_COORDS

    results: List[Dict[str, Optional[str]]] = []

    for c in city_coords:
        if not c.strip():
            continue
        try:
            city, coords = c.split(":")
            lat_str, lon_str = coords.split(",")
            lat, lon = float(lat_str), float(lon_str)
        except ValueError:
            print(f"❌ Skipping invalid entry: {c}")
            continue

        res = _fetch_city(city, lat, lon)
        results.append(res)
        time.sleep(SLEEP_BETWEEN_CALLS)

    return results

# --- CLI Execution ---
if __name__ == "__main__":
    print("Starting extraction for AtmosTrack Air Quality API")
    print(f"Cities: {CITY_COORDS}")
    out = fetch_all_cities()
    print("Extraction complete. Summary:")
    for r in out:
        if r.get("success") == "true":
            print(f" - {r['city']}: saved -> {r['raw_path']}")
        else:
            print(f" - {r['city']}: ERROR -> {r.get('error')}")
