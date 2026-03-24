"""
receiver.py

Utilities for receiving and validating protocol frames over serial.

Responsibilities:
    - Read a binary frame from the serial port, discarding noise before START byte
    - Parse raw bytes into a structured dictionary
    - Validate frame integrity via CRC-16 checksum
    - Display a received frame in a readable format
"""

import QAT

def read_frame(ser) -> bytes | None:
    """
    Read one complete protocol frame from a serial port.

    Scans for the START byte (0xAA), discarding any preceding bytes
    such as ESP-IDF debug logs. Once found, reads the 3-byte header
    to determine SIZE, then reads the remaining payload and CRC bytes.

    Args:
        ser (serial.Serial): An open serial port instance.

    Returns:
        bytes: Complete raw frame, or None if a timeout occurs.
    """
    # Scan for START byte, discarding any noise
    while True:
        byte = ser.read(1)
        if not byte:
            return None
        if byte[0] == QAT.START:
            break

    # Read TYPE, PERIPHERAL and SIZE
    header = ser.read(3)
    if len(header) < 3:
        return None

    size = header[2]

    # Read PAYLOAD + CRC (2 bytes)
    body = ser.read(size + 2)
    if len(body) < size + 2:
        return None

    return bytes([QAT.START]) + header + body


def parse_packet(data: bytes) -> dict:
    """
    Parse a raw frame into a structured dictionary.

    Args:
        data (bytes): Complete raw frame bytes.

    Returns:
        dict: Parsed frame with keys:
            - start      (int):   START byte value.
            - type       (int):   Message type.
            - peripheral (int):   Target peripheral.
            - size       (int):   Payload length in bytes.
            - payload    (bytes): Command-specific data.
            - crc        (bytes): Received CRC (2 bytes, big-endian).
    """
    size = data[3]
    return {
        "start":      data[0],
        "type":       data[1],
        "peripheral": data[2],
        "size":       size,
        "payload":    data[4: 4 + size],
        "crc":        data[4 + size:],
    }


def check_packet(data: bytes) -> bool:
    """
    Validate the CRC-16 of a received frame.

    Computes the CRC over all bytes from START through the last
    PAYLOAD byte, and compares it against the received CRC bytes.

    Args:
        data (bytes): Complete raw frame bytes.

    Returns:
        bool: True if the computed CRC matches the received CRC,
              False otherwise.
    """
    if len(data) < 6:
        return False

    size = data[3]
    frame_body = data[:4 + size]
    received_crc = int.from_bytes(data[4 + size:], "big")
    computed_crc = QAT.crc_calc(frame_body)

    return computed_crc == received_crc


def print_frame(frame: dict) -> None:
    """
    Display a parsed frame dictionary in a readable format.

    Args:
        frame (dict): Output of parse_packet().

    Returns:
        None
    """
    print("--- Received frame ---")
    print(f"START:      0x{frame['start']:02X}")
    print(f"TYPE:       0x{frame['type']:02X}")
    print(f"PERIPHERAL: 0x{frame['peripheral']:02X}")
    print(f"SIZE:       {frame['size']}")
    print(f"PAYLOAD:    {frame['payload'].hex(' ').upper()}")
    print(f"CRC:        {frame['crc'].hex(' ').upper()}")