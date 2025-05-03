import random


class PowerMonitor:
    def __init__(self):
        self.voltage = 3.7

    def update_simulated_voltage(self):
        change = random.uniform(-0.01, 0.01)
        self.voltage = max(3.3, min(4.2, self.voltage + change))
        print(f"[Power] Simulated Voltage: {self.voltage:.2f}V")

    def get_voltage(self):
        return self.voltage

    def is_low(self):
        return self.voltage < 3.5
