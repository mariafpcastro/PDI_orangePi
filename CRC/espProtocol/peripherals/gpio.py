"""
gpio.py

Utilities for building and interpreting GPIO protocol messages.
"""

from ..protocol import constants as c


def gpio_config_payload(pin: int, config: int) -> bytes:
    """
    Build the payload bytes for a GPIO configuration command.

    The config byte should be one of the CONFIG_* constants
    defined in constants.py (e.g. CONFIG_OUT_PP_HIGH).

    Args:
        pin    (int): GPIO pin number.
        config (int): Configuration byte (e.g. c.CONFIG_OUT_PP_HIGH).

    Returns:
        bytes: 2-byte payload ready to pass to build_packet().

    Example:
        >>> gpio_config_payload(10, c.CONFIG_OUT_PP_HIGH)
        b'\\x0a\\x02'
    """
    return bytes([pin, config])


def gpio_read(msg_type: int, payload: bytes) -> None:
    """
    Interpret and display a GPIO response payload received from the ESP32.

    Args:
        msg_type (int):   Message type of the received frame (e.g. TYPE_READ).
        payload  (bytes): Payload bytes from the parsed frame.

    Returns:
        None
    """
    pin = payload[0]
    status = payload[1]

    if msg_type in (c.TYPE_CONFIG, c.TYPE_EVENT, c.TYPE_WRITE):
        if status == c.STATUS_OK:
            print(f"GPIO {pin} configured successfully.")
        elif status == c.STATUS_FAIL:
            print(f"GPIO {pin} configuration failed.")
        else:
            print(f"GPIO {pin} unknown status: 0x{status:02X}")

    elif msg_type == c.TYPE_READ:
        if status == 0x01:
            print(f"GPIO {pin} — logic level HIGH")
        elif status == 0x00:
            print(f"GPIO {pin} — logic level LOW")
        else:
            print(f"GPIO {pin} unknown level: 0x{status:02X}")