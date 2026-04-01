import streamlit as st
import pandas as pd
import plotly.express as px
from db import init_db, get_connection
from etl import run_etl

st.set_page_config(page_title="AirScope ETL", layout="wide")
init_db()

st.title("AirScope")
st.caption("Real air quality dashboard powered by OpenWeather ETL")

if "last_fetch_status" not in st.session_state:
    st.session_state.last_fetch_status = None

if st.button("Fetch latest data"):
    result = run_etl()
    st.session_state.last_fetch_status = result

status = st.session_state.last_fetch_status
if status:
    if status["success"]:
        st.success(
            f"{status['message']} Inserted: {status['inserted']}, skipped duplicates: {status['skipped']}."
        )
    else:
        st.error(f"ETL failed at {status['stage']} stage: {status['message']}")

conn = get_connection()
df = pd.read_sql("SELECT * FROM air_quality_measurements ORDER BY timestamp ASC", conn)
conn.close()

if df.empty:
    st.warning("No data yet. When your OpenWeather key activates, click 'Fetch latest data'.")
    st.stop()

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"]).sort_values("timestamp")

last_loaded = df["timestamp"].max()
st.info(f"Last stored measurement: {last_loaded.strftime('%Y-%m-%d %H:%M')}")

latest = df.iloc[-1]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("AQI", latest["aqi"])
c2.metric("PM2.5", latest["pm25"])
c3.metric("PM10", latest["pm10"])
c4.metric("NO2", latest["no2"])
c5.metric("O3", latest["o3"])

st.subheader("Latest trends")

col1, col2 = st.columns(2)

with col1:
    fig_pm = px.line(
        df,
        x="timestamp",
        y=["pm25", "pm10"],
        title="PM2.5 and PM10 over time",
        markers=True
    )
    fig_pm.update_layout(
        xaxis_title="Time",
        yaxis_title="Concentration"
    )
    fig_pm.update_xaxes(tickformat="%d %b\n%H:%M")
    st.plotly_chart(fig_pm, use_container_width=True)

with col2:
    fig_gases = px.line(
        df,
        x="timestamp",
        y=["no2", "o3", "so2"],
        title="Gas pollutants over time",
        markers=True
    )
    fig_gases.update_layout(
        xaxis_title="Time",
        yaxis_title="Concentration"
    )
    fig_gases.update_xaxes(tickformat="%d %b\n%H:%M")
    st.plotly_chart(fig_gases, use_container_width=True)

st.subheader("Historical views")

period = st.selectbox(
    "Select chart range",
    ["All data", "Last 24 hours", "Last 7 days", "Last 30 days"]
)

filtered_df = df.copy()

if period == "Last 24 hours":
    filtered_df = df[df["timestamp"] >= df["timestamp"].max() - pd.Timedelta(hours=24)]
elif period == "Last 7 days":
    filtered_df = df[df["timestamp"] >= df["timestamp"].max() - pd.Timedelta(days=7)]
elif period == "Last 30 days":
    filtered_df = df[df["timestamp"] >= df["timestamp"].max() - pd.Timedelta(days=30)]

if filtered_df.empty:
    st.warning("No data available for the selected period.")
else:
    fig_hist = px.line(
        filtered_df,
        x="timestamp",
        y=["aqi", "pm25", "pm10"],
        title=f"Historical air quality: {period}",
        markers=True
    )
    fig_hist.update_layout(
        xaxis_title="Time",
        yaxis_title="Value"
    )
    fig_hist.update_xaxes(tickformat="%d %b\n%H:%M")
    st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Stored measurements")

table_df = df.copy()
table_df["timestamp"] = table_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")

st.dataframe(
    table_df.sort_values("timestamp", ascending=False),
    use_container_width=True
)
