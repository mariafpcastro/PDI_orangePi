import serial
import time
import QAT

# --- Serial setup ---
# Open the serial port where the ESP32 is connected.
# Adjust the port name and baud rate to match your setup.
ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
time.sleep(1)

# --- Read pin 12 ---
# NOTE: pin must be configured via TYPE_CONFIG before any TYPE_READ command.
#
# The payload for a read command is just the pin number as a single byte.
# Replace 0x0C (decimal 12) with the pin number you want to read.
frame = QAT.send_packet(ser, QAT.TYPE_READ, QAT.PERIPHERAL_GPIO, b"\x0C", max_retries=3)

if frame:
    QAT.print_frame(frame)                         # Print the full raw frame for debugging
    QAT.gpio_read(QAT.TYPE_READ, frame["payload"]) # Interpret and display the pin level (HIGH/LOW)
else:
    print("Read failed after all retries.")
