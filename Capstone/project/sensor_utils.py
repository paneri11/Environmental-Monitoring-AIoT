# sensor_utils.py

import random
from datetime import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from bson import ObjectId  

# Simulate fake sensor readings
def simulate_sensor_data():
    return {
        "timestamp": datetime.now().isoformat(),
        "temperature": round(random.uniform(20, 40), 2),  # °C
        "humidity": round(random.uniform(30, 90), 2),     # %
        "co2": random.randint(300, 800),                  # ppm
        "air_quality": random.randint(50, 200),           # AQI
        "noise": round(random.uniform(30, 90), 2)         # dB
    }

# Fetch recent sensor documents from MongoDB
def fetch_data(collection):
    docs = list(collection.find().sort("timestamp", -1))
    if not docs:
        return pd.DataFrame()
    for doc in docs:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    df = pd.DataFrame(docs)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values('timestamp', inplace=True)
    return df


# Generate line chart for a given parameter
def plot_time_series(df, param):
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'], df[param], marker='o', color='teal')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel(param)
    ax.grid(True)
    return fig

# Predict next 10 temperature values using linear regression
def plot_temperature_forecast(df):
    X = list(range(len(df)))
    y = df['temperature'].values
    model = LinearRegression().fit([[i] for i in X], y)

    future_X = list(range(len(df), len(df) + 10))
    future_y = model.predict([[i] for i in future_X])
    # future_timestamps = [df['timestamp'].iloc[-1] + pd.Timedelta(minutes=10*(i+1)) for i in range(10)]

    fig, ax = plt.subplots()
    ax.plot(df['timestamp'], y, label="Actual Temp", marker='o', color='blue')
    ax.plot(future_timestamps, future_y, label="Predicted", linestyle='--', marker='x', color='red')
    ax.set_title("Temperature Forecast (Next 10 Readings)")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True)
    return fig
