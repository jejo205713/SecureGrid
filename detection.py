# detection.py
# GridSentinel - Real-Time Anomaly Detection Module

import json
import time
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "localhost"
TOPIC = "gridsentinel/telemetry"
ALERT_LOG_FILE = "alerts.log"

# Thresholds for anomaly detection (adjustable)
THRESHOLDS = {
    "voltage": (215, 245),       # volts
    "current": (0, 20),          # amps
    "frequency": (49.5, 50.5),   # Hz
    "temperature": (0, 85)       # °C
}

def log_alert(message):
    """Log alerts to a file with timestamps."""
    with open(ALERT_LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def is_anomaly(data):
    """Check if any telemetry value is outside thresholds."""
    for key, (low, high) in THRESHOLDS.items():
        if key in data and not (low <= data[key] <= high):
            return True, f"{key.upper()} anomaly: {data[key]} (Expected {low}-{high})"
    return False, None

def on_message(client, userdata, msg):
    """MQTT message handler."""
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        anomaly, alert_message = is_anomaly(payload)
        
        if anomaly:
            alert_text = f"🚨 ALERT: {alert_message} | Data: {payload}"
            print(alert_text)
            log_alert(alert_text)
        else:
            print(f"✅ Normal: {payload}")

    except json.JSONDecodeError:
        print("⚠️ Received invalid JSON data.")
    except Exception as e:
        print(f"❌ Error processing message: {e}")

def main():
    client = mqtt.Client()
    client.on_message = on_message

    try:
        client.connect(BROKER, 1883, 60)
    except Exception as e:
        print(f"❌ Could not connect to MQTT broker: {e}")
        return

    client.subscribe(TOPIC)
    print("🔍 GridSentinel Detection Module Started...")
    
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping detection module.")
        client.disconnect()

if __name__ == "__main__":
    main()
