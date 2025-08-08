# dashboard.py
"""
GridSentinel Dashboard Module
Provides a Flask-based web dashboard to monitor real-time
power grid metrics, anomaly alerts, and system logs.

Author: JEJO J
Date: 2025-08-08
"""

import os
import json
import threading
from flask import Flask, render_template, jsonify
from datetime import datetime

# --------------------------------------------
# Config
# --------------------------------------------
DATA_FILE = "data/metrics.json"     # Output from capture.py
ALERT_FILE = "data/alerts.json"     # Output from detection.py
PORT = int(os.environ.get("DASHBOARD_PORT", 5000))

# --------------------------------------------
# Flask App
# --------------------------------------------
app = Flask(__name__)

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def read_json_safely(file_path):
    """Safely read a JSON file, return empty list/dict on error."""
    try:
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

@app.route("/")
def index():
    """Render the dashboard homepage."""
    return render_template("dashboard.html")

@app.route("/api/metrics")
def api_metrics():
    """Return latest metrics in JSON."""
    data = read_json_safely(DATA_FILE)
    return jsonify(data)

@app.route("/api/alerts")
def api_alerts():
    """Return current alerts."""
    data = read_json_safely(ALERT_FILE)
    return jsonify(data)

def run_server():
    """Run the Flask dashboard server."""
    app.run(host="0.0.0.0", port=PORT, debug=False)

# --------------------------------------------
# HTML Template (Inline for Prototype)
# --------------------------------------------
TEMPLATE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>GridSentinel Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; background: #f5f7fa; margin: 0; padding: 0; }
        header { background: #1f2937; color: white; padding: 15px; text-align: center; }
        .container { padding: 20px; }
        canvas { background: white; border-radius: 10px; padding: 10px; }
        h2 { color: #1f2937; }
        .alerts { background: #fff3f3; padding: 10px; border-radius: 5px; }
        .alert-item { margin-bottom: 5px; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<header>
    <h1>⚡ GridSentinel Dashboard</h1>
</header>
<div class="container">
    <h2>Live Metrics</h2>
    <canvas id="metricsChart" height="100"></canvas>

    <h2>Active Alerts</h2>
    <div class="alerts" id="alertsList"></div>
</div>

<script>
async function fetchMetrics() {
    const res = await fetch('/api/metrics');
    return await res.json();
}

async function fetchAlerts() {
    const res = await fetch('/api/alerts');
    return await res.json();
}

async function updateDashboard(chart) {
    const metrics = await fetchMetrics();
    const alerts = await fetchAlerts();

    chart.data.labels = metrics.map(m => m.timestamp);
    chart.data.datasets[0].data = metrics.map(m => m.voltage);
    chart.data.datasets[1].data = metrics.map(m => m.frequency);
    chart.update();

    const alertsList = document.getElementById("alertsList");
    alertsList.innerHTML = alerts.length ? "" : "<p>No active alerts ✅</p>";
    alerts.forEach(a => {
        const div = document.createElement("div");
        div.classList.add("alert-item");
        div.innerHTML = `<strong>${a.type}</strong> - ${a.message} <br><small>${a.timestamp}</small>`;
        alertsList.appendChild(div);
    });
}

document.addEventListener("DOMContentLoaded", async () => {
    const ctx = document.getElementById('metricsChart').getContext('2d');
    const metricsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                { label: 'Voltage (V)', borderColor: 'blue', fill: false, data: [] },
                { label: 'Frequency (Hz)', borderColor: 'green', fill: false, data: [] }
            ]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: false } }
        }
    });

    // Refresh every 5 seconds
    setInterval(() => updateDashboard(metricsChart), 5000);
});
</script>
</body>
</html>
"""

# Save template on first run
template_path = os.path.join(app.root_path, "templates")
os.makedirs(template_path, exist_ok=True)
with open(os.path.join(template_path, "dashboard.html"), "w", encoding="utf-8") as f:
    f.write(TEMPLATE_HTML)

# --------------------------------------------
# Main Entry
# --------------------------------------------
if __name__ == "__main__":
    print(f"[INFO] Dashboard running at http://localhost:{PORT}")
    run_server()
