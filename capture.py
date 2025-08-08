#!/usr/bin/env python3
# capture.py
# GridSentinel - Data Capture Module
# Collects or simulates real-time grid telemetry and publishes via MQTT

import time
import random
import json
import logging
import sys
import signal
from typing import Dict
import paho.mqtt.client as mqtt

# ====== CONFIGURATION ======
BROKER = "localhost"            # MQTT broker address
PORT = 1883                     # MQTT broker port
TOPIC = "gridsentinel/telemetry"
PUBLISH_INTERVAL = 2            # Seconds between messages
SIMULATION_MODE = True          # Set to False for real sensor integration
# ============================

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Global MQTT client
client = mqtt.Client()


def generate_data() -> Dict:
    """
    Generate power grid telemetry data.
    Replace this with real sensor readings if SIMULATION_MODE is False.
    """
    return {
        "timestamp": time.time(),
        "voltage": round(random.uniform(220, 240), 2),   # Volts
        "current": round(random.uniform(5, 15), 2),      # Amps
        "frequency": round(random.uniform(49.8, 50.2), 2),  # Hz
        "temperature": round(random.uniform(25, 80), 2)  # Celsius
    }


def publish_data():
    """Generate and publish telemetry data to MQTT."""
    try:
        data = generate_data()
        payload = json.dumps(data)
        result = client.publish(TOPIC, payload, qos=1)

        # Check publish result
        status = result[0]
        if status == mqtt.MQTT_ERR_SUCCESS:
            logging.info(f"📡 Sent: {payload}")
        else:
            logging.error(f"Failed to publish message: {payload}")
    except Exception as e:
        logging.exception(f"Error while publishing data: {e}")


def connect_mqtt():
    """Connect to the MQTT broker with error handling."""
    try:
        client.connect(BROKER, PORT, keepalive=60)
        logging.info(f"✅ Connected to MQTT broker at {BROKER}:{PORT}")
    except Exception as e:
        logging.error(f"❌ Failed to connect to MQTT broker: {e}")
        sys.exit(1)


def graceful_exit(signum, frame):
    """Handle graceful shutdown on SIGINT/SIGTERM."""
    logging.info("🛑 Shutting down capture module...")
    client.loop_stop()
    client.disconnect()
    sys.exit(0)


def main():
    # Signal handlers for clean exit
    signal.signal(signal.SIGINT, graceful_exit)
    signal.signal(signal.SIGTERM, graceful_exit)

    # MQTT setup
    connect_mqtt()
    client.loop_start()

    logging.info("🚀 GridSentinel Capture Module Started.")
    try:
        while True:
            publish_data()
            time.sleep(PUBLISH_INTERVAL)
    except Exception as e:
        logging.exception(f"Unexpected error in main loop: {e}")
    finally:
        graceful_exit(None, None)


if __name__ == "__main__":
    main()
