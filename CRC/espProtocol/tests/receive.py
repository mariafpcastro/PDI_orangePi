import protocol
import utils
import serial
import time

#ser = serial.Serial("dev/ttyUSB0", 115200, timeout=1)
##time.sleep (2)

#data = ser.readline().decode().strip()
data = 'AA 01 01 02 0A 04 74 F1'

result = protocol.check_packet(data)

if result == 1:
    protocol.parse_packet(data)
    print("Os dados nao foram corrompidos. Pode decodificar")
elif result == 0:
    print('Dados corrompidos, reenvio do pacote solicitado')
else:
    print('Dados nem foram recebidos')