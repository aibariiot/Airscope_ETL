import requests
import pandas as pd
import sqlite3
from datetime import datetime, timezone
from config import OPENWEATHER_API_KEY, LAT, LON, CITY
from db import get_connection, init_db

def extract_openweather():
    url = "https://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": LAT,
        "lon": LON,
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(url, params=params, timeout=30)

    if response.status_code == 401:
        return {
            "success": False,
            "error_type": "auth",
            "message": "401 Unauthorized: API key invalid, inactive, or not yet activated.",
            "data": None
        }

    if response.status_code != 200:
        return {
            "success": False,
            "error_type": "http",
            "message": f"HTTP {response.status_code}: {response.text}",
            "data": None
        }

    try:
        data = response.json()
    except Exception:
        return {
            "success": False,
            "error_type": "parse",
            "message": "Response was not valid JSON.",
            "data": None
        }

    if "list" not in data or not data["list"]:
        return {
            "success": False,
            "error_type": "empty",
            "message": "API returned no measurements.",
            "data": None
        }

    return {
        "success": True,
        "error_type": None,
        "message": "Data extracted successfully.",
        "data": data
    }

def transform_openweather(data):
    row = data["list"][0]
    components = row["components"]

    df = pd.DataFrame([{
        "timestamp": datetime.fromtimestamp(row["dt"], tz=timezone.utc).isoformat(),
        "source": "openweather",
        "city": CITY,
        "latitude": LAT,
        "longitude": LON,
        "aqi": row["main"]["aqi"],
        "co": components.get("co"),
        "no": components.get("no"),
        "no2": components.get("no2"),
        "o3": components.get("o3"),
        "so2": components.get("so2"),
        "nh3": components.get("nh3"),
        "pm25": components.get("pm2_5"),
        "pm10": components.get("pm10"),
    }])

    return df

def load_to_sqlite(df):
    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO air_quality_measurements (
                    timestamp, source, city, latitude, longitude,
                    aqi, co, no, no2, o3, so2, nh3, pm25, pm10
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["timestamp"], row["source"], row["city"],
                row["latitude"], row["longitude"],
                row["aqi"], row["co"], row["no"], row["no2"],
                row["o3"], row["so2"], row["nh3"], row["pm25"], row["pm10"]
            ))
            inserted += 1
        except sqlite3.IntegrityError:
            skipped += 1

    conn.commit()
    conn.close()

    return inserted, skipped

def run_etl():
    init_db()

    extracted = extract_openweather()
    if not extracted["success"]:
        return {
            "success": False,
            "stage": "extract",
            "message": extracted["message"],
            "inserted": 0,
            "skipped": 0
        }

    df = transform_openweather(extracted["data"])
    inserted, skipped = load_to_sqlite(df)

    return {
        "success": True,
        "stage": "load",
        "message": "ETL completed successfully.",
        "inserted": inserted,
        "skipped": skipped
    }

if __name__ == "__main__":
    result = run_etl()
    print(result)
