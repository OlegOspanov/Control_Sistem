import time

class AlertState:
    def __init__(self, duration = 3.0):
        self.duration = duration
        self.last_time = 0.0

    def trigger(self):
        self.last_time = time.time()

    def active(self):
        return time.time() - self.last_time < self.duration