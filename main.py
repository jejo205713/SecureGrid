#!/usr/bin/env python3
"""
SecureGrid - Main Orchestrator
Author: JEJO J
Description:
    Master controller for SecureGrid – an AI-driven, blockchain-secured
    smart grid anomaly detection and response system.
"""

import asyncio
import logging
import signal
import sys
from capture import capture_data
from detection import detect_anomalies
from response import respond_to_threat
from dashboard import start_dashboard

# ===== Logging Setup =====
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("SecureGrid")


# ===== Graceful Shutdown =====
shutdown_flag = False

def handle_shutdown(signal_received, frame):
    global shutdown_flag
    logger.warning("Shutdown signal received. Stopping SecureGrid...")
    shutdown_flag = True


# ===== Orchestration Logic =====
async def securegrid_loop():
    """Main AI-driven security loop"""
    logger.info("🔒 SecureGrid is live. Monitoring power grid...")

    while not shutdown_flag:
        try:
            # 1️⃣ Capture
            data = await capture_data()
            if not data:
                logger.debug("No data captured this cycle.")
                await asyncio.sleep(1)
                continue

            # 2️⃣ Detection
            threats = detect_anomalies(data)
            if threats:
                logger.warning(f"⚠ Threats detected: {threats}")

                # 3️⃣ Response
                for threat in threats:
                    respond_to_threat(threat)
            else:
                logger.info("✅ No anomalies detected this cycle.")

        except Exception as e:
            logger.error(f"Main loop error: {e}")

        await asyncio.sleep(1)  # Prevent CPU overload

    logger.info("SecureGrid shutdown complete.")


# ===== Entry Point =====
if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        # Start dashboard in background
        logger.info("Starting dashboard...")
        import threading
        threading.Thread(target=start_dashboard, daemon=True).start()

        # Run main loop
        asyncio.run(securegrid_loop())

    except KeyboardInterrupt:
        handle_shutdown(None, None)
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        sys.exit(1)
