import requests
import time
import random

# The URL of your teammate's Flask API
API_URL = "http://localhost:5000/api/status" 

def send_telemetry(device_type, packet_size, latency, fails):
    data = {
        "device_type": device_type,
        "packet_size_bytes": packet_size,
        "latency_ms": latency,
        "failed_login_attempts": fails,
        "connection_count": random.randint(1, 5),
        "data_rate_mbps": random.uniform(0.1, 5.0)
    }
    try:
        response = requests.post("http://localhost:5000/api/status", json=data)
        print(f"Sent: {data} | API Response: {response.json()}")
    except Exception as e:
        print(f"Error: Could not connect to API. Is Flask running? {e}")

# --- TEST 1: NORMAL BEHAVIOR (Everything stays GREEN) ---
print("\n--- Phase 1: Sending Normal Traffic (Safe) ---")
for _ in range(3):
    send_telemetry("Smart_Light", 500, 20, 0)
    time.sleep(1)

# --- TEST 2: THE ANOMALY (Trust Score should DROP to RED) ---
print("\n--- Phase 2: Launching a Simulated ATTACK! ---")
# We send a HUGE packet and HIGH latency
send_telemetry("Smart_Light", 9999, 800, 15)


# import joblib
# import pandas as pd
# import numpy as np
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# # 1. Initialize the Flask App
# app = Flask(__name__)

# CORS(app)

# # 2. Load the trained model
# # The file was just created in the previous step
# MODEL_PATH = 'iott_security_model_v2.joblib'
# try:
#     loaded_model = joblib.load(MODEL_PATH)
#     print(f"Successfully loaded model from {MODEL_PATH}")
# except FileNotFoundError:
#     print("Error: Model file still not found. Please ensure cell bb4b40af finished.")

# # 3. Define the API route
# @app.route('/api/status', methods=['POST'])
# def get_trust_status():
#     try:
#         # Get JSON data from the request
#         data = request.get_json()
        
#         # Prepare data for model
#         input_features = ['packet_size_bytes', 'latency_ms', 'connection_count', 'data_rate_mbps']
#         df_input = pd.DataFrame([data], columns=input_features)
        
#         # Get Raw Anomaly Score
#         raw_score = loaded_model.decision_function(df_input)[0]
        
#         # Scaling Logic (Mapping to 0-100)
#         # Using standard ranges for the Isolation Forest output
#         trust_score = np.interp(raw_score, (-0.2, 0.1), (0, 100))
#         trust_score = int(round(trust_score))
        
#         # Evidence Log / Status
#         status = "✅ SAFE" if trust_score >= 50 else "❌ RISKY"
        
#         return jsonify({
#             "trust_score": trust_score,
#             "status": status,
#             "evidence_log": {
#                 "raw_anomaly_score": float(raw_score),
#                 "packet_size": data.get('packet_size_bytes'),
#                 "latency": data.get('latency_ms')
#             }
#         })
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# if __name__ == '__main__':
#     print("API Bridge starting on http://localhost:5000/api/status")
#     app.run(port=5000)