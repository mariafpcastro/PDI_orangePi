import espProtocol as ep
import serial
import time

#   Inicializando a porta serial 
ser = serial.Serial("/dev/ttyUSB0", 1_000_000, timeout=1)
time.sleep(1)
 
 
#   Escolhendo o comando pelo terminal
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

#   Printa cada parte do pacote
print('Start: ', ep.START)
print('Type: ', type_msg)
print('Peripheral: ', per_msg)
print('Size: ', size)
print('payload: ', payload)

#   Faz o pacote completo em byte, ja com o crc 
pacote = ep.build_packet(type_msg, per_msg, payload)

#   Imprime o pacote que sera enviado
ep.print_packet(pacote)

#   Envia o pacote para a ESP
ser.write(pacote)
 

print("Aguardando resposta da ESP...")
 
ep.parse_packet()
