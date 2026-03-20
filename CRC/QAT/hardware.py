import os
class DeviceInterface:
    def __init__(self, pin):
        self.pin = pin
        self.is_embedded = os.uname().machine.startswith(('arm', 'aarch'))
    def set_pin_state(self, state):
        label = "HIGH" if state else "LOW"
        print(f"[{'HW REAL' if self.is_embedded else 'MOCK'}] Pino {self.pin} -> {label}")
