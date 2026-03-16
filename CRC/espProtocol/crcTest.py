import protocol
import utils

dados = [0xAA, 0x03, 0x01, 0x02, 0x16, 0x01]

crc = protocol.crc_calc(dados)

crc16 = utils.to_hex(crc)

print(crc16)

crc16 = utils.to_bytes(crc)

print (crc16)
