import serial
import time

import QAT

# --- Serial setup ---
ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
time.sleep(1)

# --- Pin 4 configuration ---
# NOTE: before any TYPE_WRITE or TYPE_READ command, the pin must be
# configured via TYPE_CONFIG, otherwise the ESP32 will acknowledge
# the comman but the hardware will not behave as expected.
# packet = QAT.build_packet(QAT.TYPE_CONFIG, QAT.PERIPHERAL_GPIO, QAT.gpio_config_write_payload(12, QAT.CONFIG_IN_NI_NP))
# ser.write(packet)
# QAT.read_frame(ser)

# --- Read pin 4 ---
type_msg = QAT.TYPE_READ
per_msg = QAT.PERIPHERAL_GPIO

packet = QAT.build_packet(type_msg, per_msg, b"\x0C")
ser.write(packet)
raw = QAT.read_frame(ser)

if raw is None:
    print("Timeout — no response received.")
elif not QAT.check_packet(raw):
    print("CRC error — corrupted frame.")
else:
    frame = QAT.parse_packet(raw)
    QAT.gpio_check(raw, 3, type_msg)