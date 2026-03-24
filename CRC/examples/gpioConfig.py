import serial
import time
import QAT

# --- Serial setup ---
# Open the serial port where the ESP32 is connected.
# Adjust the port name and baud rate to match your setup.
ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
time.sleep(1)

# --- Pin 12 configuration ---
# Build the payload with the pin number and the desired configuration.
# Replace CONFIG_IN_NI_NP with any CONFIG_* constant from constants.py
# to match your intended pin direction, resistor and trigger settings.
type_msg = QAT.TYPE_CONFIG
per_msg = QAT.PERIPHERAL_GPIO
payload = QAT.gpio_config_write_payload(12, QAT.CONFIG_IN_NI_NP)

# Send the configuration packet and wait for the ESP32 response.
# send_packet handles building, sending, CRC validation and retries automatically.
frame = QAT.send_packet(ser, type_msg, per_msg, payload, 3)

if frame:
    QAT.print_frame(frame)                           # Print the full raw frame for debugging
    QAT.gpio_read(QAT.TYPE_CONFIG, frame["payload"]) # Interpret and display the ESP32 status
else:
    print("Configuration failed after all retries.")