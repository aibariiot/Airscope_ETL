import sqlite3
from config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS air_quality_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,
            city TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            aqi INTEGER,
            co REAL,
            no REAL,
            no2 REAL,
            o3 REAL,
            so2 REAL,
            nh3 REAL,
            pm25 REAL,
            pm10 REAL,
            UNIQUE(timestamp, source, city)
        )
    """)

    conn.commit()
    conn.close()
