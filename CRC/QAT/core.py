from .hardware import DeviceInterface
class SensorController:
    def __init__(self, pin=18):
        self.hw = DeviceInterface(pin)
    def run_alert(self):
        self.hw.set_pin_state(True)
        return True
