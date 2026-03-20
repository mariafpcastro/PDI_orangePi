import serial
import time

import QAT

# --- Serial setup ---
ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
time.sleep(1)

# --- Pin 4 configuration ---
type_msg = QAT.TYPE_CONFIG
per_msg = QAT.PERIPHERAL_GPIO
payload = QAT.gpio_config_write_payload(4, QAT.CONFIG_OUT_PP_HIGH)

packet = QAT.build_packet(type_msg, per_msg, payload)

packet = packet[:-2] + bytes([0xDE, 0xAD])

ser.write(packet)

raw = QAT.read_frame(ser)

if raw is None:
    print("Timeout — no response received.")
elif not QAT.check_packet(raw):
    print("CRC error — corrupted frame.")
else:
    frame = QAT.parse_packet(raw)
    QAT.print_frame(frame) # displays the full received frame for debugging
    QAT.gpio_read(type_msg, frame["payload"])