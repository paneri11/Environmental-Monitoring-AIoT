# streamlit_app.py

import streamlit as st
import pymongo
from sensor_utils import (
    simulate_sensor_data,
    fetch_data,
    plot_time_series,
    plot_temperature_forecast
)

# Configure page
st.set_page_config(page_title="Environmental AIoT Dashboard", layout="wide")

# MongoDB connection
MONGO_URI = st.secrets["MONGO_URI"]
client = pymongo.MongoClient(MONGO_URI)
db = client["env_db"]
collection = db["sensor_data"]

# Title and header
st.title("🌱 Environmental Monitoring Dashboard using AIoT")
st.markdown("Real-time data tracking and prediction using simulated sensors and AI.")

# Insert simulated data
if st.button("➕ Insert Simulated Sensor Data"):
    data = simulate_sensor_data()
    collection.insert_one(data)
    st.success("Simulated sensor data inserted into MongoDB!")

# Fetch latest sensor data
df = fetch_data(collection)

# Raw data view
if st.checkbox("Show Raw Sensor Data"):
    st.dataframe(df)

# If data available, plot trends and predictions
if not df.empty:
    st.subheader("📈 Parameter Trends Over Time")
    col1, col2 = st.columns(2)
    parameters = ['temperature', 'humidity', 'air_quality', 'co2', 'noise']

    for i, param in enumerate(parameters):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"#### {param.replace('_', ' ').title()}")
            fig = plot_time_series(df, param)
            st.pyplot(fig)

    st.subheader("🤖 AI Temperature Prediction")
    fig2 = plot_temperature_forecast(df)
    st.pyplot(fig2)

    st.subheader("📊 Current Sensor Readings")
    latest = df.iloc[-1]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🌡 Temperature (°C)", f"{latest['temperature']:.2f}")
    c2.metric("💧 Humidity (%)", f"{latest['humidity']:.2f}")
    c3.metric("🌀 AQI", f"{latest['air_quality']:.2f}")
    c4.metric("🫁 CO₂ (ppm)", f"{latest['co2']:.2f}")
    c5.metric("🔊 Noise (dB)", f"{latest['noise']:.2f}")
else:
    st.warning("No data available in MongoDB. Please insert some simulated data.")
