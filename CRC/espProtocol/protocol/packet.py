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
import serial, time

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

def parse_packet():
    ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
    time.sleep(1)

    start_byte = b''
    while True:
        start_byte = ser.read(1)
        if not start_byte:
            break
        if start_byte[0] == 0xAA:
            break
 
    if not start_byte or start_byte[0] != 0xAA:
        print("Nenhuma resposta recebida (timeout aguardando START 0xAA)")
 
    # Lê TYPE, PERIPHERAL e SIZE (3 bytes restantes do cabeçalho)
    cabecalho = ser.read(3)
 
    if len(cabecalho) < 3:
        print("Nenhuma resposta recebida (timeout no cabecalho)")
    else:
        type_resp   = cabecalho[0]
        periph_resp = cabecalho[1]
        size_resp   = cabecalho[2]
 
        corpo = ser.read(size_resp + 2)  # payload + 2 bytes de CRC
 
        if len(corpo) < size_resp + 2:
            print("Resposta incompleta (timeout no corpo)")
        else:
            payload_resp = corpo[:size_resp]
            crc_resp     = corpo[size_resp:]
 
            print("--- Resposta recebida ---")
            print(f"START:      0xAA")
            print(f"TYPE:       0x{type_resp:02X}")
            print(f"PERIPHERAL: 0x{periph_resp:02X}")
            print(f"SIZE:       {size_resp}")
            print(f"PAYLOAD:    {payload_resp.hex(' ').upper()}")
            print(f"CRC:        {crc_resp.hex(' ').upper()}")
 
            # Verifica o status retornado pela ESP32 (payload[1] = 0x00 OK / 0xFF erro)
            if size_resp >= 2:
                status = payload_resp[1]
                if status == 0x00:
                    print("Status: OK")
                elif status == 0xFF:
                    print("Status: ERRO (ESP32 recusou o comando)")
                else:
                    print(f"Status: 0x{status:02X} (nivel lido)")


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
    