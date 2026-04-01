# AirScope

AirScope is a Python-based air quality monitoring dashboard built with Streamlit.

The project uses an ETL pipeline to fetch air pollution data from the OpenWeather Air Pollution API, transform the API response into a structured format, store the data in SQLite, and visualize it in an interactive dashboard. The goal of the project is to demonstrate a small but complete data engineering workflow: extraction, transformation, loading, storage, and visualization.

## Project goal

The main goal of AirScope is to simulate a real-world monitoring system using external environmental data. Instead of relying on local hardware sensors, the project collects air quality measurements from an API source and builds a historical dashboard on top of the stored data.

This project was designed as a student project to demonstrate:
- API integration
- ETL pipeline design
- SQLite-based storage
- duplicate prevention
- dashboard building with Streamlit
- basic automation support

## Features

- Fetches real air pollution data from the OpenWeather API
- Stores data in SQLite
- Prevents duplicate inserts using a unique constraint
- Handles API failures and invalid responses gracefully
- Displays current KPI values in a dashboard
- Shows historical pollutant trends with Plotly charts
- Supports repeated execution for data accumulation over time

## Architecture

The data flow is:

OpenWeather API -> ETL pipeline -> SQLite database -> Streamlit dashboard

### Components

- `etl.py`  
  Extracts data from the API, transforms the JSON response, and loads the result into SQLite.

- `db.py`  
  Initializes the database and defines the table schema.

- `config.py`  
  Reads configuration values such as API key, coordinates, and city name.

- `app.py`  
  Streamlit dashboard for visualizing stored measurements.

## Project structure

```text
AirScope/
├── app.py
├── etl.py
├── db.py
├── config.py
├── README.md
├── .env.example
└── air_quality.db
```


## Requirements:
-Python 3.10+ recommended

-OpenWeather API key

This project requires a personal OpenWeather API key for live data fetching.
Create an account and generate a key here: https://openweathermap.org/api/air-pollution

Important: 
A newly created key may not work immediately. 
OpenWeather may return  401 Unauthorized  until the key is fully activated.

## clone the repo
git clone https://github.com/aibariiot/Airscope_ETL.git

cd Airscope_ETL

## create venv
python -m venv .venv

source .venv/bin/activate


## dependencies 
pip install streamlit pandas plotly requests python-dotenv

## create .env in root 
OPENWEATHER_API_KEY=your_api_key_here
LAT=50.0755
LON=14.4378
CITY=Prague
DB_PATH=air_quality.db


## run etl
python etl.py

##start the dashboard
streamlit run app.py


