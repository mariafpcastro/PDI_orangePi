import serial
import time

import QAT

# --- Serial setup ---
ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
time.sleep(1)

# --- Pin configuration ---
# NOTE: before any TYPE_WRITE or TYPE_READ command, the pin must be
# configured via TYPE_CONFIG, otherwise the ESP32 will acknowledge
# the command but the hardware will not behave as expected.
#packet = QAT.build_packet(QAT.TYPE_CONFIG, QAT.PERIPHERAL_GPIO, QAT.gpio_config_write_payload(4, QAT.CONFIG_OUT_PP_LOW))
#ser.write(packet)
#raw = QAT.read_frame(ser)   # wait for ESP32 to acknowledge before proceeding

# --- Write pin 4 ---
type_msg = QAT.TYPE_WRITE
per_msg = QAT.PERIPHERAL_GPIO
payload = QAT.gpio_config_write_payload(12, 1)

packet = QAT.build_packet(type_msg, per_msg, payload)
ser.write(packet)


QAT.gpio_check(ser, packet, 3, type_msg)

# if raw is None:
#     print("Timeout — no response received.")
# elif not QAT.check_packet(raw):
#     print("CRC error — corrupted frame.")
# else:
#     frame = QAT.parse_packet(raw)
#     QAT.print_frame(frame)   # displays the full received frame for debugging
#     QAT.gpio_read(type_msg, frame["payload"])