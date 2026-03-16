"""
packet.py

Packet construction and parsing utilities for the communication protocol.

Frame (Packet) structure
Offset(Byte) | Field      | Size    | Description
0            | START      | 1 byte  | Fixed value 0xAA. Indicates the start of a new packet.
1            | TYPE       | 1 byte  | Defines the message type (Configuration, Read, Event, etc.).
2            | PERIPHERAL | 1 byte  | Indicates the target peripheral (GPIO, I2C, DAC) or 0xFF for System.
3            | SIZE (N)   | 1 byte  | Size of the payload field in bytes (0–255).
4 to 4+N-1   | PAYLOAD    | N bytes | Command-specific data. If SIZE = 0, this field does not exist.
4+N          | CRC_H      | 1 byte  | High byte (MSB) of the CRC-16 checksum.
5+N          | CRC_L      | 1 byte  | Low byte (LSB) of the CRC-16 checksum

The CRC is calculated over all bytes from START to the last byte of PAYLOAD.
"""

from . import constants
from . import crc
from .. import utils

def build_packet(msg_type: int, peripheral: int, payload: bytes = b"") -> bytes:
    #Docstring
    """
    Build a protocol packet according to the defined frame structure.

    Frame format:
        START | TYPE | PERIPHERAL | SIZE | PAYLOAD | CRC_H | CRC_L

    Args:
        msg_type (int): Message type identifier.
        peripheral (int): Target peripheral identifier.
        payload (bytes, optional): Command-specific data. Defaults to empty.

    Returns:
        bytes: Encoded packet ready for transmission.
    """

    size = len(payload)

    frame = [constants.START, msg_type, peripheral, size] +  list(payload)

    crc_value = crc.crc_calc(frame)

    packet = bytes(frame) + crc_value.to_bytes(2, "big")

    return packet

def parse_packet(data):
    
    dados = data.split(" ")
    print (dados)

    start = dados[0]
    type = dados[1]
    peripheral = dados[2]
    size = int(dados[3])
    i=0
    payload = []
    while i<size:
        payload.append( dados[4+i])
        i += 1 

    print("START: ", start)
    print("TYPE: ", type)
    print("PERIPHERAL: ", peripheral)
    print("SIZE: ", size)
    print("PAYLOAD: ", payload)


def check_packet(data):
    
    dados = data[:-6]
    crc = data[-5:]

    if data:
        dados = bytes.fromhex(dados)
        crc = bytes.fromhex(crc)
    else:
            return -1
    
    SOS = crc.crc_calc(dados)

    SOS = utils.to_bytes(SOS)

    if SOS == crc:
        return 1
    else:
        return 0
    