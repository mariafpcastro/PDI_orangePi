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

import QAT

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

    frame = [QAT.START, msg_type, peripheral, size] +  list(payload)

    crc_value = QAT.crc_calc(frame)

    packet = bytes(frame) + crc_value.to_bytes(2, "big")

    return packet


def send_packet(ser, msg_type: int, peripheral: int, payload: bytes = b"", max_retries: int = 3) -> dict | None:
    """
    Build, send, and validate a packet, retrying on error frames or timeouts.

    Args:
        ser         : open serial.Serial instance.
        msg_type    : message type (e.g. TYPE_WRITE).
        peripheral  : target peripheral (e.g. PERIPHERAL_GPIO).
        payload     : command-specific data.
        max_retries : how many attempts before giving up.

    Returns:
        dict : parsed frame on success, or None if all attempts failed.
    """
    packet = build_packet(msg_type, peripheral, payload)

    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt}/{max_retries}...")
        ser.write(packet)
        raw = QAT.read_frame(ser)

        if raw is None:
            print("Timeout — no response received.")
            continue
        if not QAT.check_packet(raw):
            print("CRC error — corrupted frame.")
            continue

        frame = QAT.parse_packet(raw)
        if frame["type"] == QAT.TYPE_ERROR:
            print("ESP32 returned an error frame. Retrying...")
            continue

        return frame  # success

    print(f"Failed after {max_retries} attempts.")
    return None
