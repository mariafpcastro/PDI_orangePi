"""
packet.py

Packet construction utility for the communication protocol.

Frame structure:
    Offset | Field      | Size    | Description
    0      | START      | 1 byte  | Fixed 0xAA — start of packet.
    1      | TYPE       | 1 byte  | Message type (Config, Read, Write, Event).
    2      | PERIPHERAL | 1 byte  | Target peripheral (GPIO, DAC, Modbus, System).
    3      | SIZE (N)   | 1 byte  | Payload length in bytes (0–255).
    4..4+N | PAYLOAD    | N bytes | Command-specific data. Absent when SIZE = 0.
    4+N    | CRC_H      | 1 byte  | High byte (MSB) of CRC-16.
    5+N    | CRC_L      | 1 byte  | Low byte (LSB) of CRC-16.

The CRC covers all bytes from START trought the last PAYLOAD byte.
"""

from . import constants
from . import crc

def build_packet(msg_type: int, peripheral: int, payload: bytes = b"") -> bytes:
    """
    Build a protocol packet ready for transmission.

    Args:
        msg_type   (int):   Message type identifier (e.g. TYPE_WRITE).
        peripheral (int):   Target peripheral identifier (e.g. PERIPHERAL_GPIO).
        payload    (bytes): Command-specific data. Defaults to empty.

    Returns:
        bytes: Fully encoded packet (header + payload + CRC).
    """

    size = len(payload)

    frame = [constants.START, msg_type, peripheral, size] +  list(payload)

    crc_value = crc.crc_calc(frame)

    packet = bytes(frame) + crc_value.to_bytes(2, "big")

    return packet

