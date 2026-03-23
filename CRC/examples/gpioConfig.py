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

QAT.gpio_check(packet, 3, type_msg)



'''
ser.write(packet)

raw = QAT.read_frame(ser)

if raw is None:
    print("Timeout — no response received.")
elif not QAT.check_packet(raw):
    print("CRC error — corrupted frame.")
else:
    frame = QAT.parse_packet(raw)
    QAT.print_frame(frame) # displays the full received frame for debugging

    if frame ["type"] == QAT.TYPE_ERROR:
        print(f"ESP32 returned an error frame.")
    elif frame["type"] == type_msg and frame["size"] >= 2:
        QAT.gpio_read(type_msg, frame["payload"])'''