import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
LAT = float(os.getenv("LAT", 50.0755))
LON = float(os.getenv("LON", 14.4378))
CITY = os.getenv("CITY", "Prague")
DB_PATH = "air_quality.db"
