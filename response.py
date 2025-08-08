# response.py
# GridSentinel - Automated Mitigation & Response Module

import json
import time
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "localhost"
ALERT_TOPIC = "gridsentinel/alerts"   # detection.py should publish here
CONTROL_TOPIC = "gridsentinel/control"
RESPONSE_LOG_FILE = "responses.log"

# Define action severity mapping
SEVERITY_ACTIONS = {
    "critical": "SHUTDOWN",
    "warning": "REDUCE_LOAD"
}

def log_response(message):
    """Log response actions to a file with timestamps."""
    with open(RESPONSE_LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def classify_alert(alert_message):
    """Classify alert severity based on keywords or parameter deviation."""
    if "voltage" in alert_message.lower() or "frequency" in alert_message.lower():
        return "critical"
    elif "temperature" in alert_message.lower() or "current" in alert_message.lower():
        return "warning"
    return "warning"

def trigger_action(client, severity, alert_data):
    """Trigger mitigation action based on severity."""
    action = SEVERITY_ACTIONS.get(severity, "MONITOR")
    control_payload = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "reason": alert_data
    }
    try:
        client.publish(CONTROL_TOPIC, json.dumps(control_payload))
        log_response(f"Action: {action} | Reason: {alert_data}")
        print(f"⚡ Executed {action} for {severity.upper()} alert.")
    except Exception as e:
        print(f"❌ Failed to send control signal: {e}")

def on_message(client, userdata, msg):
    """MQTT message handler."""
    try:
        alert_data = json.loads(msg.payload.decode("utf-8"))
        severity = classify_alert(alert_data.get("message", ""))
        trigger_action(client, severity, alert_data)
    except json.JSONDecodeError:
        print("⚠️ Invalid alert JSON received.")
    except Exception as e:
        print(f"❌ Error processing alert: {e}")

def main():
    client = mqtt.Client()
    client.on_message = on_message

    try:
        client.connect(BROKER, 1883, 60)
    except Exception as e:
        print(f"❌ Could not connect to MQTT broker: {e}")
        return

    client.subscribe(ALERT_TOPIC)
    print("🛡️ GridSentinel Response Module Started...")
    
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping response module.")
        client.disconnect()

if __name__ == "__main__":
    main()
