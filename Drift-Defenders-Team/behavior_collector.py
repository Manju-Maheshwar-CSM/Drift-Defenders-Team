from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
import numpy as np
from datetime import datetime
import time
import os

# -------------------------------
# CONFIGURATION
# -------------------------------
DEVICE_IPS = ["192.168.1.101", "192.168.1.102"]
OUTPUT_FILE = "iot_network_behavior_dataset.csv"
WINDOW_SIZE = 10  # seconds

# Create output file if not exists
if not os.path.exists(OUTPUT_FILE):
    df = pd.DataFrame(columns=[
        "timestamp",
        "device_ip",
        "packet_size_bytes",
        "latency_ms",
        "connection_count",
        "data_rate_mbps",
        "label"
    ])
    df.to_csv(OUTPUT_FILE, index=False)

# Temporary storage for window
packet_buffer = []


# -------------------------------
# PACKET CAPTURE FUNCTION
# -------------------------------
def process_packet(packet):
    if IP in packet:
        src_ip = packet[IP].src

        if src_ip in DEVICE_IPS:
            packet_buffer.append({
                "timestamp": datetime.now(),
                "device_ip": src_ip,
                "packet_size": len(packet)
            })


# -------------------------------
# AGGREGATION FUNCTION
# -------------------------------
def aggregate_and_save():
    global packet_buffer

    if len(packet_buffer) == 0:
        return

    df = pd.DataFrame(packet_buffer)

    for device in df["device_ip"].unique():

        device_data = df[df["device_ip"] == device]

        connection_count = len(device_data)

        total_bytes = device_data["packet_size"].sum()

        avg_packet_size = device_data["packet_size"].mean()

        # Data rate in Mbps
        data_rate_mbps = (total_bytes * 8) / (WINDOW_SIZE * 1_000_000)

        # Simulated latency (since passive sniffing can't measure real latency easily)
        latency_ms = np.random.uniform(10, 100)

        # Assume normal during baseline collection
        label = "normal"

        new_row = pd.DataFrame([{
            "timestamp": datetime.now(),
            "device_ip": device,
            "packet_size_bytes": avg_packet_size,
            "latency_ms": latency_ms,
            "connection_count": connection_count,
            "data_rate_mbps": data_rate_mbps,
            "label": label
        }])

        new_row.to_csv(OUTPUT_FILE, mode="a", header=False, index=False)

        print(f"[Aggregated] {device} | Conn:{connection_count} | Rate:{round(data_rate_mbps,4)} Mbps")

    packet_buffer = []  # Clear buffer


# -------------------------------
# MAIN LOOP
# -------------------------------
print("Listening to IoT devices and aggregating every 10 seconds...")

start_time = time.time()

def packet_handler(packet):
    process_packet(packet)

    global start_time
    if time.time() - start_time >= WINDOW_SIZE:
        aggregate_and_save()
        start_time = time.time()


sniff(prn=packet_handler, store=False)