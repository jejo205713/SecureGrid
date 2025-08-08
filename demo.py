# demo.py
import time
import random
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

ATTACKS = [
    "DDoS attack on SCADA servers",
    "Malware injection in control systems",
    "False data injection to mislead operators",
    "Unauthorized remote access attempt",
    "Insider threat – suspicious commands",
    "Phishing compromise of admin credentials"
]

RESPONSES = [
    "Isolating affected node...",
    "Blocking malicious IPs...",
    "Rolling back to last safe configuration...",
    "Alerting security team...",
    "Switching to backup control channel..."
]

def simulate_telemetry():
    return {
        "voltage": round(random.uniform(210, 250), 2),
        "current": round(random.uniform(10, 100), 2),
        "frequency": round(random.uniform(49.5, 50.5), 2),
        "status": random.choice(["Normal", "Slight anomaly", "Critical anomaly"])
    }

def display_intro():
    console.print("[bold green]⚡ SecureGrid – AI-Driven Cyber-Physical Defense Simulation ⚡[/bold green]\n")
    console.print("This is a simulation of SecureGrid detecting and responding to threats in a smart power grid.\n")

def run_demo():
    display_intro()

    # Show fake telemetry updates
    for _ in track(range(5), description="Collecting live telemetry..."):
        data = simulate_telemetry()
        console.print(f"[cyan]{datetime.now().strftime('%H:%M:%S')}[/cyan] | Voltage: {data['voltage']}V | Current: {data['current']}A | Frequency: {data['frequency']}Hz | Status: {data['status']}")
        time.sleep(0.8)

    console.print("\n[bold yellow]🚨 ALERT! Possible intrusion detected...[/bold yellow]\n")
    time.sleep(1)

    # Pick a random attack
    attack = random.choice(ATTACKS)
    console.print(f"[red]Detected Threat:[/red] {attack}")
    time.sleep(1)

    # Fake AI confidence
    confidence = random.uniform(85, 99)
    console.print(f"[blue]AI Confidence:[/blue] {confidence:.2f}%")
    time.sleep(1)

    # Show automated response
    console.print("\n[bold green]Initiating Automated Response...[/bold green]")
    for step in RESPONSES:
        console.print(f"[green]✔[/green] {step}")
        time.sleep(0.8)

    console.print("\n[bold cyan]📜 Logging event to blockchain for forensic analysis...[/bold cyan]")
    time.sleep(1.5)

    console.print("\n[bold green]✅ Simulation Complete – SecureGrid successfully neutralized the threat.[/bold green]\n")

if __name__ == "__main__":
    run_demo()
