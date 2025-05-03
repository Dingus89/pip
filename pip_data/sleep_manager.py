# sleep_manager.py

import time
from pip_core_drives import PipCoreDrives
from repair_log import log_issue


class SleepManager:
    def __init__(self, core_drives: PipCoreDrives):
        self.core = core_drives
        self.sleeping = False
        self.last_active_time = time.time()
        self.sleep_threshold = 120  # seconds of idle before sleeping
        self.energy_threshold = 20  # energy level that triggers sleep
        self.wake_sensors = {
            "pir": False,
            "touch": False,
            "voice": False
        }

    def update_activity(self):
        self.last_active_time = time.time()
        if self.sleeping:
            self.wake_up("active input")

    def should_sleep(self):
        if self.core.energy < self.energy_threshold:
            return True
        if (time.time() - self.last_active_time) > self.sleep_threshold:
            return True
        return False

    def enter_sleep(self):
        if not self.sleeping:
            print("[SleepManager] Entering sleep mode.")
            self.sleeping = True
            self.core.energy += 0.5  # slowly regain energy while sleeping
            self.core.fade_emotions()
            return True
        return False

    def wake_up(self, reason):
        if self.sleeping:
            print(f"[SleepManager] Waking up due to: {reason}")
            self.sleeping = False
            self.core.energy -= 1  # small energy cost to wake
            self.update_activity()

    def process(self):
        if self.sleeping:
            if self.wake_sensors["pir" or "touch" or "voice"]:
                self.wake_up("sensor trigger")
        elif self.should_sleep():
            self.enter_sleep()

    def set_wake_sensor(self, sensor: str, triggered: bool):
        if sensor in self.wake_sensors:
            self.wake_sensors[sensor] = triggered
            if triggered:
                self.update_activity()
        else:
            log_issue(f"Unknown wake sensor: {sensor}")
