'''import espProtocol as ep
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 1000000, timeout=1)



#---------------------------------------------------------------------------------------------------------------------------
#   ESCOLHENDO O QUE FAZER ANTES DE MANDAR PARA A ESP
#---------------------------------------------------------------------------------------------------------------------------
print('Vamos enviar comandos para a Esp! Primeiro, me diga o tipo de mensagem')

while(1):
    print('1. Configuracao')
    print('2. Leitura')
    print('3. Escrita')
    print('4. Evento')
    type = int(input('Insira apenas o numero do evento! '))
    
    if (type == 1):
        type_msg = ep.TYPE_CONFIG
        break
    elif (type == 2):
        type_msg = ep.TYPE_READ
        break
    elif (type == 3):
        type_msg = ep.TYPE_WRITE
        break
    elif (type == 3):
        type_msg = ep.TYPE_EVENT
        break
    else:
        print ('Por favor, insira um valor valido!')

print('Agora, escolha o periferico a ser comandado')
while (1):
    print('1. GPIO')
    print('2. DAC')
    print('3. Modbus')
    print('4. Sistema/Global')
    per = int(input('Insira apenas o numero do evento! '))
    if per == 1:
        per_msg = ep.PERIPHERAL_GPIO
        break
    elif per == 2:
        per_msg = ep.PERIPHERAL_DAC
        break
    elif per == 3:
        per_msg = ep.PERIPHERAL_MODBUS
        break
    elif per == 4:
        per_msg = ep.PERIPHERAL_SYS
        break
    else:
        print ('Por favor, insira um valor valido!')

payl = []
if per_msg == ep.PERIPHERAL_GPIO and type_msg == ep.TYPE_CONFIG:
    size = 2
    payl.append(int(input("Insira o pino que deseja comandar: ")))
    print("")
    print("Agora vamos configurar!")
    print("1. Saida")
    print("2. Entrada")
    Direcao = int(input("Escolha a direcao do pino: "))
    print("")
    if Direcao==1:
        print("Tipo de resistor:")
        print("1. Open-drain")
        print("2. Push-pull")
        Resistor = int(input("Selecione o tipo de resistor: "))
        print("Nivel")
        print("1. High")
        print("2. Low")
        Trigger = int(input("Selecione o Trigger: "))
        if Resistor==1 and Trigger==1:
            indice = 1
        elif Resistor==2 and Trigger==1:
            indice = 2
        if Resistor==1 and Trigger==2:
            indice = 3
        elif Resistor==2 and Trigger==2:
            indice = 4


    elif Direcao==2:
        print("1. Sem interrupcao")
        print("2. Com interrupcao")
        Interrupcao = int(input("Selecione se há interrupcao ou nao"))
        print("Tipo de resistor:")
        print("1. Pull-up")
        print("2. Pull-down")
        print("3. No-pull")
        Resistor = int(input("Selecione o tipo de resistor: "))
        print("Nivel")
        print("1. Rising")
        print("2. Falling")
        print("3. Both")
        Trigger = int(input("Selecione o Nivel: "))
        if Interrupcao==1 and Resistor==1:
            indice=5
        elif Interrupcao==1 and Resistor==2:
            indice=6
        elif Interrupcao==1 and Resistor==3:
            indice=7
        elif Interrupcao==2 and Resistor==1 and Trigger==1:
            indice=8
        elif Interrupcao==2 and Resistor==1 and Trigger==2:
            indice=9
        elif Interrupcao==2 and Resistor==1 and Trigger==3:
            indice=10
        elif Interrupcao==2 and Resistor==2 and Trigger==1:
            indice=11
        elif Interrupcao==2 and Resistor==2 and Trigger==2:
            indice=12
        elif Interrupcao==2 and Resistor==2 and Trigger==3:
            indice=13
        elif Interrupcao==2 and Resistor==3 and Trigger==1:
            indice=14
        elif Interrupcao==2 and Resistor==3 and Trigger==2:
            indice=15
        elif Interrupcao==2 and Resistor==3 and Trigger==3:
            indice=16
        
    payl.append(indice)
else:
    size = int(input('Insira o tamanho do seu Payload: '))
    i = 0
    while i < size:
        payl.append(int(input(f'Insira o termo {i+1} do seu payload ')))
        i+=1

payload = bytearray(payl)

print('Start: ', ep.START)
print('Type: ', type_msg)
print('Peripheral: ', per_msg)
print('Size: ', size)
print('payload: ', payload)

pacote = ep.build_packet(type_msg, per_msg, payload)

PACOTE = ep.print_packet(pacote)

print (PACOTE)

print (pacote)

ser.write(pacote)

print("Aguardando resposta da ESP...")
    
time.sleep (2)
    
resposta = ser.readline().decode().strip()

if resposta:
    print(resposta)
else:
    print("Nenhuma resposta recebida")

'''

'''
import espProtocol as ep
import serial
import time

# [CORRIGIDO] Baud rate alterado de 115200 para 1.000.000 bps,
# conforme definido em uart_comm.h (UART_BAUD_RATE = 1_000_000).
# Com 115200 o firmware recebia lixo ou nada.
ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
time.sleep(1)


#---------------------------------------------------------------------------------------------------------------------------
#   ESCOLHENDO O QUE FAZER ANTES DE MANDAR PARA A ESP
#---------------------------------------------------------------------------------------------------------------------------
print('Vamos enviar comandos para a Esp! Primeiro, me diga o tipo de mensagem')

while(1):
    print('1. Configuracao')
    print('2. Leitura')
    print('3. Escrita')
    print('4. Evento')
    type = int(input('Insira apenas o numero do evento! '))

    if (type == 1):
        type_msg = ep.TYPE_CONFIG
        break
    elif (type == 2):
        type_msg = ep.TYPE_READ
        break
    elif (type == 3):
        type_msg = ep.TYPE_WRITE
        break
    # [CORRIGIDO] Condição era (type == 3), igual ao WRITE acima,
    # então EVENT nunca era alcançado. Corrigido para (type == 4).
    elif (type == 4):
        type_msg = ep.TYPE_EVENT
        break
    else:
        print('Por favor, insira um valor valido!')

print('Agora, escolha o periferico a ser comandado')
while (1):
    print('1. GPIO')
    print('2. DAC')
    print('3. Modbus')
    print('4. Sistema/Global')
    per = int(input('Insira apenas o numero do evento! '))
    if per == 1:
        per_msg = ep.PERIPHERAL_GPIO
        break
    elif per == 2:
        per_msg = ep.PERIPHERAL_DAC
        break
    elif per == 3:
        per_msg = ep.PERIPHERAL_MODBUS
        break
    elif per == 4:
        per_msg = ep.PERIPHERAL_SYS
        break
    else:
        print('Por favor, insira um valor valido!')

payl = []
if per_msg == ep.PERIPHERAL_GPIO and type_msg == ep.TYPE_CONFIG:
    size = 2
    payl.append(int(input("Insira o pino que deseja comandar: ")))
    print("")
    print("Agora vamos configurar!")
    print("1. Saida")
    print("2. Entrada")
    Direcao = int(input("Escolha a direcao do pino: "))
    print("")
    if Direcao == 1:
        print("Tipo de resistor:")
        print("1. Open-drain")
        print("2. Push-pull")
        Resistor = int(input("Selecione o tipo de resistor: "))
        print("Nivel")
        print("1. High")
        print("2. Low")
        Trigger = int(input("Selecione o Trigger: "))
        if Resistor == 1 and Trigger == 1:
            indice = 1
        elif Resistor == 2 and Trigger == 1:
            indice = 2
        elif Resistor == 1 and Trigger == 2:
            indice = 3
        elif Resistor == 2 and Trigger == 2:
            indice = 4

    elif Direcao == 2:
        print("1. Sem interrupcao")
        print("2. Com interrupcao")
        Interrupcao = int(input("Selecione se há interrupcao ou nao: "))
        print("Tipo de resistor:")
        print("1. Pull-up")
        print("2. Pull-down")
        print("3. No-pull")
        Resistor = int(input("Selecione o tipo de resistor: "))
        print("Nivel")
        print("1. Rising")
        print("2. Falling")
        print("3. Both")
        Trigger = int(input("Selecione o Nivel: "))
        if Interrupcao == 1 and Resistor == 1:
            indice = 5
        elif Interrupcao == 1 and Resistor == 2:
            indice = 6
        elif Interrupcao == 1 and Resistor == 3:
            indice = 7
        elif Interrupcao == 2 and Resistor == 1 and Trigger == 1:
            indice = 8
        elif Interrupcao == 2 and Resistor == 1 and Trigger == 2:
            indice = 9
        elif Interrupcao == 2 and Resistor == 1 and Trigger == 3:
            indice = 10
        elif Interrupcao == 2 and Resistor == 2 and Trigger == 1:
            indice = 11
        elif Interrupcao == 2 and Resistor == 2 and Trigger == 2:
            indice = 12
        elif Interrupcao == 2 and Resistor == 2 and Trigger == 3:
            indice = 13
        elif Interrupcao == 2 and Resistor == 3 and Trigger == 1:
            indice = 14
        elif Interrupcao == 2 and Resistor == 3 and Trigger == 2:
            indice = 15
        elif Interrupcao == 2 and Resistor == 3 and Trigger == 3:
            indice = 16

    payl.append(indice)
else:
    size = int(input('Insira o tamanho do seu Payload: '))
    i = 0
    while i < size:
        payl.append(int(input(f'Insira o termo {i+1} do seu payload ')))
        i += 1

payload = bytearray(payl)

print('Start: ', ep.START)
print('Type: ', type_msg)
print('Peripheral: ', per_msg)
print('Size: ', size)
print('payload: ', payload)

pacote = ep.build_packet(type_msg, per_msg, payload)

PACOTE = ep.print_packet(pacote)

print(PACOTE)

print(pacote)

ser.write(pacote)

# [CORRIGIDO] Recepção reescrita para leitura binária do frame QAT.
#
# O problema original usava ser.readline().decode().strip(), que aguarda
# um caractere '\n' que nunca chega — a ESP32 envia frames binários com
# tamanho variável, não linhas de texto. Isso fazia a leitura sempre
# bloquear até o timeout e retornar vazio.
#
# O protocolo QAT define o frame como:
#   [ START(1) | TYPE(1) | PERIPHERAL(1) | SIZE(1) | PAYLOAD(SIZE) | CRC_H(1) | CRC_L(1) ]
# O campo SIZE informa quantos bytes de payload virão a seguir, por isso
# lemos o cabeçalho primeiro e depois completamos com payload + CRC.
print("Aguardando resposta da ESP...")

cabecalho = ser.read(4)

if len(cabecalho) < 4:
    print("Nenhuma resposta recebida (timeout no cabecalho)")
else:
    start_byte  = cabecalho[0]
    type_resp   = cabecalho[1]
    periph_resp = cabecalho[2]
    size_resp   = cabecalho[3]

    corpo = ser.read(size_resp + 2)  # payload + 2 bytes de CRC

    if len(corpo) < size_resp + 2:
        print("Resposta incompleta (timeout no corpo)")
    else:
        payload_resp = corpo[:size_resp]
        crc_resp     = corpo[size_resp:]

        print("--- Resposta recebida ---")
        print(f"START:      0x{start_byte:02X}")
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
'''


import espProtocol as ep
import serial
import time
 
ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
time.sleep(1)
 
 
#---------------------------------------------------------------------------------------------------------------------------
#   ESCOLHENDO O QUE FAZER ANTES DE MANDAR PARA A ESP
#---------------------------------------------------------------------------------------------------------------------------
print('Vamos enviar comandos para a Esp! Primeiro, me diga o tipo de mensagem')
 
while(1):
    print('1. Configuracao')
    print('2. Leitura')
    print('3. Escrita')
    print('4. Evento')
    type = int(input('Insira apenas o numero do evento! '))
 
    if (type == 1):
        type_msg = ep.TYPE_CONFIG
        break
    elif (type == 2):
        type_msg = ep.TYPE_READ
        break
    elif (type == 3):
        type_msg = ep.TYPE_WRITE
        break
    elif (type == 4):
        type_msg = ep.TYPE_EVENT
        break
    else:
        print('Por favor, insira um valor valido!')
 
print('Agora, escolha o periferico a ser comandado')
while (1):
    print('1. GPIO')
    print('2. DAC')
    print('3. Modbus')
    print('4. Sistema/Global')
    per = int(input('Insira apenas o numero do evento! '))
    if per == 1:
        per_msg = ep.PERIPHERAL_GPIO
        break
    elif per == 2:
        per_msg = ep.PERIPHERAL_DAC
        break
    elif per == 3:
        per_msg = ep.PERIPHERAL_MODBUS
        break
    elif per == 4:
        per_msg = ep.PERIPHERAL_SYS
        break
    else:
        print('Por favor, insira um valor valido!')
 
payl = []
if per_msg == ep.PERIPHERAL_GPIO and type_msg == ep.TYPE_CONFIG:
    size = 2
    payl.append(int(input("Insira o pino que deseja comandar: ")))
    print("")
    print("Agora vamos configurar!")
    print("1. Saida")
    print("2. Entrada")
    Direcao = int(input("Escolha a direcao do pino: "))
    print("")
    if Direcao == 1:
        print("Tipo de resistor:")
        print("1. Open-drain")
        print("2. Push-pull")
        Resistor = int(input("Selecione o tipo de resistor: "))
        print("Nivel")
        print("1. High")
        print("2. Low")
        Trigger = int(input("Selecione o Trigger: "))
        if Resistor == 1 and Trigger == 1:
            indice = 1
        elif Resistor == 2 and Trigger == 1:
            indice = 2
        elif Resistor == 1 and Trigger == 2:
            indice = 3
        elif Resistor == 2 and Trigger == 2:
            indice = 4
 
    elif Direcao == 2:
        print("1. Sem interrupcao")
        print("2. Com interrupcao")
        Interrupcao = int(input("Selecione se há interrupcao ou nao: "))
        print("Tipo de resistor:")
        print("1. Pull-up")
        print("2. Pull-down")
        print("3. No-pull")
        Resistor = int(input("Selecione o tipo de resistor: "))
        print("Nivel")
        print("1. Rising")
        print("2. Falling")
        print("3. Both")
        Trigger = int(input("Selecione o Nivel: "))
        if Interrupcao == 1 and Resistor == 1:
            indice = 5
        elif Interrupcao == 1 and Resistor == 2:
            indice = 6
        elif Interrupcao == 1 and Resistor == 3:
            indice = 7
        elif Interrupcao == 2 and Resistor == 1 and Trigger == 1:
            indice = 8
        elif Interrupcao == 2 and Resistor == 1 and Trigger == 2:
            indice = 9
        elif Interrupcao == 2 and Resistor == 1 and Trigger == 3:
            indice = 10
        elif Interrupcao == 2 and Resistor == 2 and Trigger == 1:
            indice = 11
        elif Interrupcao == 2 and Resistor == 2 and Trigger == 2:
            indice = 12
        elif Interrupcao == 2 and Resistor == 2 and Trigger == 3:
            indice = 13
        elif Interrupcao == 2 and Resistor == 3 and Trigger == 1:
            indice = 14
        elif Interrupcao == 2 and Resistor == 3 and Trigger == 2:
            indice = 15
        elif Interrupcao == 2 and Resistor == 3 and Trigger == 3:
            indice = 16
 
    payl.append(indice)
elif per_msg == ep.PERIPHERAL_GPIO and type_msg == ep.TYPE_WRITE:
    size = 2
    payl.append(int(input("Insira o pino que deseja comandar: ")))
    payl.append(int(input("Insira 0 para LED OFF e 1 para LED ON: ")))
else:
    size = int(input('Insira o tamanho do seu Payload: '))
    i = 0
    while i < size:
        payl.append(int(input(f'Insira o termo {i+1} do seu payload ')))
        i += 1
 
payload = bytearray(payl)
 
print('Start: ', ep.START)
print('Type: ', type_msg)
print('Peripheral: ', per_msg)
print('Size: ', size)
print('payload: ', payload)
 
pacote = ep.build_packet(type_msg, per_msg, payload)
 
ep.print_packet(pacote)
 
print(pacote)
 
ser.write(pacote)
 
# [CORRIGIDO] Recepção reescrita para leitura binária do frame QAT.
#
# O problema original usava ser.readline().decode().strip(), que aguarda
# um caractere '\n' que nunca chega — a ESP32 envia frames binários com
# tamanho variável, não linhas de texto. Isso fazia a leitura sempre
# bloquear até o timeout e retornar vazio.
#
# O protocolo QAT define o frame como:
#   [ START(1) | TYPE(1) | PERIPHERAL(1) | SIZE(1) | PAYLOAD(SIZE) | CRC_H(1) | CRC_L(1) ]
# O campo SIZE informa quantos bytes de payload virão a seguir, por isso
# lemos o cabeçalho primeiro e depois completamos com payload + CRC.
#
# [CORRIGIDO] A recepção agora busca o byte START (0xAA) antes de
# interpretar o frame. Isso descarta logs de debug do ESP-IDF que chegam
# pela mesma UART misturados com os frames binários. Sem essa busca, o
# código interpretava o primeiro byte de um log de texto como cabeçalho.
print("Aguardando resposta da ESP...")
 
# Busca o byte START (0xAA), descartando qualquer byte anterior (logs, ruído)
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