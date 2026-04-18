import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

# 1. Load your brilliant ChatGPT dataset
df = pd.read_csv('iot_network_behavior_dataset.csv')

# 2. We only care about the numbers (the network telemetry)
# We will look at Packet Size, Latency, and Connections
features = ['packet_size_bytes', 'latency_ms', 'connection_count', 'data_rate_mbps']

# 3. GATED LEARNING (Slide 10 Strategy)
# We train the AI ONLY on the "normal" data so it knows what peace looks like!
normal_data = df[df['label'] == 'normal']
X_train = normal_data[features]

print("Training the AI on Normal IoT behavior...")
# 4. Initialize the Brain: The Isolation Forest
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X_train)
print("Training Complete! The AI is now guarding the network.\n")

import joblib

# Save trained model
joblib.dump(model, "iott_security_model_v2.joblib")

print("Model saved as iott_security_model_v2.joblib")

# --- THE LIVE DEMO TEST ---
# Let's test it on a random mix of 10 rows (some normal, some attacks)
test_data = df.sample(10, random_state=99)
X_test = test_data[features]

# The AI scores the traffic.
# It outputs scores from around -0.5 (High Risk) to 0.5 (Very Safe)
anomaly_scores = model.decision_function(X_test)

# 5. Convert to your "Trust Score (0-100)" exactly as promised on Slide 7!
# We do some quick math to map the score to a 0-100 scale.
trust_scores = np.interp(anomaly_scores, (anomaly_scores.min(), anomaly_scores.max()), (0, 100))

# Show the results!
test_data['AI_Trust_Score'] = trust_scores.round()

# Create a simple "SAFE / RISKY" tag based on your rule (Score < 50 is Risky)
test_data['Dashboard_Status'] = test_data['AI_Trust_Score'].apply(lambda x: " SAFE" if x >= 50 else " RISKY")

print("--- SECURITY DASHBOARD OUTPUT ---")
print(test_data[['device_type', 'label', 'AI_Trust_Score', 'Dashboard_Status']])