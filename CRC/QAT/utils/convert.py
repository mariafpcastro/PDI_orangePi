# convert.py

def to_hex(value: int) -> str:
    """
    Convert an integer value to a hexadecimal string.

    Args:
        value (int): Integer value to convert.

    Returns:
        str: Hexadecimal string representation (e.g. '0x1a2b').
    """
    return hex(value)

def to_bytes(value: int) -> bytes:
    """
    Convert an integer CRC value to a 2-byte big-endian bytes object.

    Args:
        value (int): Integer value to convert (16-bit).

    Returns:
        bytes: 2-byte big-endian representation.
    """
    return value.to_bytes(2, "big")