import serial
import time
import QAT

# --- Serial setup ---
# Open the serial port where the ESP32 is connected.
# Adjust the port name and baud rate to match your setup.
ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
time.sleep(1)

# --- Write pin 12 ---
# NOTE: pin must be configured via TYPE_CONFIG before any TYPE_WRITE command.
#
# Build the payload with the pin number and the desired output level.
# Second argument: 1 = HIGH, 0 = LOW.
payload = QAT.gpio_config_write_payload(12, 1)

# Send the write packet and wait for the ESP32 response.
# send_packet handles building, sending, CRC validation and retries automatically.
frame = QAT.send_packet(ser, QAT.TYPE_WRITE, QAT.PERIPHERAL_GPIO, payload, max_retries=3)

if frame:
    QAT.print_frame(frame)                          # Print the full raw frame for debugging
    QAT.gpio_read(QAT.TYPE_WRITE, frame["payload"]) # Interpret and display the ESP32 status
else:
    print("Write failed after all retries.")