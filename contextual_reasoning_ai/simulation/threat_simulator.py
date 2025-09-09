import random
import time
from datetime import datetime

class ThreatSimulator:
    def __init__(self):
        self.sample_threats = [
            {"type": "Phishing", "vector": "Email", "severity": 6},
            {"type": "Ransomware", "vector": "Executable", "severity": 9},
            {"type": "DDoS", "vector": "Network", "severity": 7},
            {"type": "Insider Threat", "vector": "User Behavior", "severity": 8},
            {"type": "Supply Chain", "vector": "Third-Party", "severity": 5},
        ]

    def simulate(self, count=5, delay=1.5):
        print(f"[{datetime.now()}] Starting Threat Simulation...")
        for _ in range(count):
            threat = random.choice(self.sample_threats)
            print(f"[{datetime.now()}] Simulated Threat: {threat['type']} via {threat['vector']} (Severity: {threat['severity']}/10)")
            time.sleep(delay)
        print(f"[{datetime.now()}] Threat Simulation Complete.")