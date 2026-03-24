"""
gpio.py

Utilities for building and interpreting GPIO protocol messages.
"""

from ..protocol import constants as c
import serial, time
import QAT


def gpio_config_write_payload(pin: int, value: int) -> bytes:
    """
    Build the payload bytes for a GPIO configuration or write command.

    The meaning of the message depends on the message type being sent:

        TYPE_CONFIG - value should be one of the CONFIG_* constants
                      defined in constants.py
                      e.g. gpio_config_write_payload(4, c.CONFIG_OUT_PP_HIGH)

        TYPE_WRITE  - value shoul be the output level:
                      0 = LOW , 1 = HIGH.
                      e.g. gpio_config_write_payload(4, 1)

    Args:
        pin   (int): GPIO pin number.
        value (int): Configuration byte (CONFIG_*) or output level (0/1).

    Returns:
        bytes: 2-byte payload ready to pass to build_packet().
    """
    return bytes([pin, value])


def gpio_read(msg_type: int, payload: bytes) -> None:
    """
    Interpret and display a GPIO response payload received from the ESP32.

    Args:
        msg_type (int):   Message type of the received frame (e.g. TYPE_READ).
        payload  (bytes): Payload bytes from the parsed frame.

    Returns:
        None
    """

    if len(payload) < 2:
        print(f"GPIO response error - payload too short ({len(payload)} byte(s)).")
        return

    pin = payload[0]
    status = payload[1]

    if msg_type in (c.TYPE_CONFIG, c.TYPE_WRITE):
        if status == c.STATUS_OK:
            print(f"GPIO {pin} configured successfully.")
        elif status == c.STATUS_FAIL:
            print(f"GPIO {pin} configuration failed.")
        else:
            print(f"GPIO {pin} unknown status: 0x{status:02X}")

    elif msg_type in (c.TYPE_READ, c.TYPE_EVENT) :
        if status == 0x01:
            print(f"GPIO {pin} — logic level HIGH")
        elif status == 0x00:
            print(f"GPIO {pin} — logic level LOW")
        else:
            print(f"GPIO {pin} unknown level: 0x{status:02X}")

def gpio_check(ser, packet, MAX_RETRIES, type_msg):

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Attempt {attempt}/{MAX_RETRIES}...")
        ser.write(packet)
        raw = QAT.read_frame(ser)

        if raw is None:
            print("Timeout — no response received.")
            continue

        if not QAT.check_packet(raw):
            print("CRC error — corrupted frame. Retrying...")
            continue

        frame = QAT.parse_packet(raw)
        QAT.print_frame(frame)

        if frame["type"] == QAT.TYPE_ERROR:
            print("ESP32 returned an error frame. Retrying...")
            continue

        if frame["size"] >= 2 and frame["payload"][1] == QAT.STATUS_FAIL:
            print("ESP32 reported failure. Retrying...")
            continue

        if frame["size"] >= 2:
            QAT.gpio_read(type_msg, frame["payload"])
        break

    else:
        print(f"Failed after {MAX_RETRIES} attempts.")


# def gpio_check(ser, packet, MAX_RETRIES, type_msg):
#     for attempt in range(1, MAX_RETRIES + 1):
#         print(f"Attempt {attempt}/{MAX_RETRIES}...")

#         # Na primeira tentativa usa o raw já recebido, depois reenvia
#         if attempt > 1:
#             ser.write(packet)
#             raw = QAT.read_frame(ser)

#         if raw is None:
#             print("Timeout — no response received.")
#             continue
#         if not QAT.check_packet(raw):
#             print("CRC error — corrupted frame. Retrying...")
#             continue

#         frame = QAT.parse_packet(raw)
#         QAT.print_frame(frame)

#         if frame["type"] == QAT.TYPE_ERROR:
#             print("ESP32 returned an error frame. Retrying...")
#             continue
#         if frame["size"] >= 2 and frame["payload"][1] == QAT.STATUS_FAIL:
#             print("ESP32 reported failure. Retrying...")
#             continue
#         if frame["size"] >= 2:
#             QAT.gpio_read(type_msg, frame["payload"])
#             break
#     else:
#         print(f"Failed after {MAX_RETRIES} attempts.")