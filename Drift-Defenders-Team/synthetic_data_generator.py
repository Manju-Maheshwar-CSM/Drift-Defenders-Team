import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

OUTPUT_FILE = "iot_network_behavior_dataset.csv"
NUM_SAMPLES = 1000

data = []

start_time = datetime.now()

for i in range(NUM_SAMPLES):

    timestamp = start_time + timedelta(seconds=i * 10)

    # Randomly choose device
    device_type = random.choice(["weather_sensor", "soil_monitor"])

    # 85% normal, 15% attack
    if random.random() < 0.85:
        label = "normal"

        packet_size_bytes = np.random.normal(300, 40)
        latency_ms = np.random.normal(50, 10)
        connection_count = np.random.normal(8, 2)
        data_rate_mbps = np.random.normal(0.2, 0.05)

    else:
        label = "attack"

        packet_size_bytes = np.random.normal(1200, 200)
        latency_ms = np.random.normal(300, 80)
        connection_count = np.random.normal(40, 10)
        data_rate_mbps = np.random.normal(3, 0.8)

    data.append([
        timestamp,
        device_type,
        abs(packet_size_bytes),
        abs(latency_ms),
        abs(connection_count),
        abs(data_rate_mbps),
        label
    ])

df = pd.DataFrame(data, columns=[
    "timestamp",
    "device_type",
    "packet_size_bytes",
    "latency_ms",
    "connection_count",
    "data_rate_mbps",
    "label"
])

df.to_csv(OUTPUT_FILE, index=False)

print(f"Synthetic dataset generated: {OUTPUT_FILE}")
print(df.head())