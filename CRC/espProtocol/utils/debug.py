def print_hex(data):
    print(" ".join(f"{b:02X}" for b in data))

def print_packet(packet: bytes):
    print(" ".join(f"{b:02X}" for b in packet))