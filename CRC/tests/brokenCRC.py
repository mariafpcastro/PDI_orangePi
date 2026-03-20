import serial
import time

import QAT as ep

ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=3)
time.sleep(2)

# Monta o pacote normalmente
packet = ep.build_packet(ep.TYPE_WRITE, ep.PERIPHERAL_GPIO, bytes([0x0A, 0x01]))

# Corrompe os últimos 2 bytes (CRC)
bad_packet = packet[:-2] + bytes([0xDE, 0xAD])

print("Pacote original: ", packet.hex(' ').upper())
print("Pacote corrompido:", bad_packet.hex(' ').upper())

ser.write(bad_packet)
print("\nPacote com CRC errado enviado. Aguardando resposta da ESP32...")

time.sleep(1)
available = ser.in_waiting
print(f"Bytes disponíveis: {available}")

if available:
    raw = ser.read(available)
    print(f"Resposta: {raw.hex(' ').upper()}")
else:
    print("Nenhuma resposta recebida.")