import time
import random

class SensorInputSimulator:
    def __init__(self):
        self.examples = [
            "Unusual traffic from 192.168.1.100",
            "User Alice accessed admin panel",
            "Detected CVE-2023-4567 on node 10.0.0.22",
            "Login failure from unknown IP",
            "High CPU usage on device 192.168.1.12"
        ]

    def stream(self):
        while True:
            yield random.choice(self.examples)
            time.sleep(1)  # Simulate real-time interval
