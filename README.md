# ⚡ SecureGrid – AI & Blockchain-Powered Power Grid Security

## 🚨 Problem Statement

Critical power grid infrastructure is increasingly targeted by cyber-physical attacks. Over the past decade, several incidents have demonstrated how vulnerabilities in grid control systems can disrupt entire nations:

- **Ukraine Power Grid Cyberattack (2015)** – Left **230,000+** people without power for hours after hackers breached SCADA systems.
- **Industroyer/CrashOverride Malware (2016)** – Specifically designed to disrupt electrical substations, cutting power to thousands.
- **Florida Water Plant Attack (2021)** – While targeting water treatment, it proved industrial control systems (ICS) are vulnerable to remote manipulation.

Such attacks threaten not only **economic stability** but also **public safety**, making **real-time anomaly detection, identity verification, and automated response** a necessity — not a luxury.

---

## 🛡 About SecureGrid

**SecureGrid** is an **AI-powered, blockchain-secured** framework to protect smart power grids from cyber threats.  
It provides **real-time anomaly detection**, **secure device authentication**, and **immutable logging**, ensuring **resilience, transparency, and rapid response**.

### ✨ Key Features
- **Real-Time Data Capture** – Continuously collects grid telemetry from IoT/SCADA sensors.
- **AI-Powered Threat Detection** – Machine learning models flag anomalies instantly.
- **Blockchain Identity Security** – Devices and operators are verified via cryptographic identities.
- **Automated Incident Response** – Isolates compromised nodes and alerts operators.
- **Interactive Dashboard** – Visualizes threats, device status, and historical logs.

---

## 📂 Project Structure

```

SecureGrid/
│
├── capture.py      # Data capture from sensors and network
├── detection.py    # AI/ML threat detection logic
├── response.py     # Automated incident response mechanisms
├── dashboard.py    # Real-time dashboard with plots and alerts
├── main.py         # Master orchestrator – runs the entire system
├── requirements.txt
└── README.md

````

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/SecureGrid.git
cd SecureGrid
````

### 2️⃣ Install Dependencies

It’s recommended to use a **virtual environment**.

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Set Environment Variables

Create a `.env` file in the root directory:

```ini
BLOCKCHAIN_NODE=http://localhost:8545
DEVICE_AUTH_KEY=your_device_private_key
```

### 4️⃣ Run SecureGrid

```bash
python main.py
```

The dashboard will be available at **[http://localhost:8050](http://localhost:8050)**

---

## 🖥 Dashboard Preview

*(Add screenshot here once ready)*

---

## 🛠 Tech Stack

* **Python** (Flask, Dash, scikit-learn, cryptography)
* **Blockchain Integration** (Ethereum testnet-ready)
* **AI/ML** (Anomaly detection with scikit-learn)
* **Data Visualization** (Plotly Dash)
* **Secure Networking** (aiohttp, psutil)

---

## 📜 License

This project is licensed under the **SecureGrid Custom License** – ensuring it remains open for research but protected from malicious use.

---

## 🤝 Contributing

We welcome contributions for:

* Improved detection models
* Better visualization components
* Expanding device simulation

Fork, branch, commit, and make a PR!

---

## 📢 Disclaimer

SecureGrid is for **educational and research purposes only**.
Deploying to live production environments without regulatory approval is **not recommended**.

---
