import serial
import time
import sys
import os

# add the parent directory to the path so espProtocol can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import QAT as ep

# --- Serial setup ---
ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
time.sleep(1)

# --- Pin 4 configuration ---
# NOTE: before any TYPE_WRITE or TYPE_READ command, the pin must be
# configured via TYPE_CONFIG, otherwise the ESP32 will acknowledge
# the comman but the hardware will not behave as expected.
packet = ep.build_packet(ep.TYPE_CONFIG, ep.PERIPHERAL_GPIO, ep.gpio_config_write_payload(4, ep.CONFIG_IN_NI_NP))
ser.write(packet)
ep.read_frame(ser)

# --- Read pin 4 ---
type_msg = ep.TYPE_READ
per_msg = ep.PERIPHERAL_GPIO

packet = ep.build_packet(type_msg, per_msg, b"\x04")
ser.write(packet)
raw = ep.read_frame(ser)

if raw is None:
    print("Timeout — no response received.")
elif not ep.check_packet(raw):
    print("CRC error — corrupted frame.")
else:
    frame = ep.parse_packet(raw)
    ep.gpio_read(type_msg, frame["payload"])
