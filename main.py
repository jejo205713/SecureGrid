#!/usr/bin/env python3
"""
GridSentinel: Main Orchestration Script
---------------------------------------
This script is the brain of the prototype.
It coordinates data capture, anomaly detection, automated response,
and dashboard updates for smart power grid cybersecurity.
"""

import sys
import time
import logging
import threading
from queue import Queue, Empty
from datetime import datetime

# Import project modules
import capture
import detection
import response
import dashboard

# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    filename="gridsentinel.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# -----------------------------
# Master Controller Class
# -----------------------------
class GridSentinelController:
    def __init__(self):
        self.event_queue = Queue()
        self.shutdown_flag = threading.Event()

    def start_capture(self):
        """Starts packet capture in a separate thread."""
        def capture_thread():
            try:
                for packet in capture.start_capture():
                    if self.shutdown_flag.is_set():
                        break
                    self.event_queue.put(packet)
            except Exception as e:
                logging.error(f"Capture module error: {e}")
        
        threading.Thread(target=capture_thread, daemon=True).start()
        logging.info("Capture module started.")

    def start_detection(self):
        """Starts detection loop in a separate thread."""
        def detection_thread():
            try:
                while not self.shutdown_flag.is_set():
                    try:
                        packet = self.event_queue.get(timeout=1)
                        result = detection.analyze_packet(packet)
                        if result.get("alert"):
                            logging.warning(f"Threat detected: {result}")
                            response.take_action(result)
                            dashboard.update_dashboard(result)
                        self.event_queue.task_done()
                    except Empty:
                        continue
            except Exception as e:
                logging.error(f"Detection module error: {e}")
        
        threading.Thread(target=detection_thread, daemon=True).start()
        logging.info("Detection module started.")

    def run(self):
        """Main control loop."""
        logging.info("GridSentinel is starting...")
        print("⚡ GridSentinel Master Controller ⚡")
        print("Starting modules...")

        self.start_capture()
        self.start_detection()

        try:
            while not self.shutdown_flag.is_set():
                time.sleep(0.5)
        except KeyboardInterrupt:
            logging.info("Shutdown signal received (Ctrl+C).")
            self.shutdown()

    def shutdown(self):
        """Gracefully shuts down all modules."""
        logging.info("Shutting down GridSentinel...")
        self.shutdown_flag.set()
        time.sleep(1)  # Allow threads to exit
        logging.info("Shutdown complete.")
        print("✅ GridSentinel stopped.")

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    controller = GridSentinelController()
    controller.run()
