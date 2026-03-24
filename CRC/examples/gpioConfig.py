import serial
import time

import QAT

# --- Serial setup ---
ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
time.sleep(1)

# --- Pin 4 configuration ---
type_msg = QAT.TYPE_CONFIG
per_msg = QAT.PERIPHERAL_GPIO
payload = QAT.gpio_config_write_payload(12, QAT.CONFIG_IN_NI_NP)

packet = QAT.build_packet(type_msg, per_msg, payload)

QAT.gpio_check(ser, packet, 3, type_msg)
