def log_issue(message):
    with open("repair_log.txt", "a") as log_file:
        log_file.write(message + "\n")


def get_last_issues(count=5):
    try:
        with open("repair_log.txt", "r") as log_file:
            lines = log_file.readlines()
            return lines[-count:]
    except FileNotFoundError:
        return []


def get_voltage(self):
    return self.voltage


def is_low(self):
    return self.voltage < 3.5
