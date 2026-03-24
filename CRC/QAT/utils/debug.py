def print_packet(packet: bytes) -> None:
    """
    Print a protocol packet as a space-separated uppercase hex string.

    Args:
        packet (bytes): Encoded packet to print.

    Returns:
        None
    """

    print(" ".join(f"{b:02X}" for b in packet))