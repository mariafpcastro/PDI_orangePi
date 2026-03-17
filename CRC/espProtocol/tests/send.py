import protocol
import utils

print('Vamos enviar comandos para a Esp! Primeiro, me diga o tipo de mensagem')

while(1):
    print('1. Configuracao')
    print('2. Leitura')
    print('3. Escrita')
    print('4. Evento')
    type = int(input('Insira apenas o numero do evento! '))
    
    if (type == 1):
        type_msg = protocol.TYPE_CONFIG
        break
    elif (type == 2):
        type_msg = protocol.TYPE_READ
        break
    elif (type == 3):
        type_msg = protocol.TYPE_WRITE
        break
    elif (type == 3):
        type_msg = protocol.TYPE_EVENT
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
        per_msg = protocol.PERIPHERAL_GPIO
        break
    elif per == 2:
        per_msg = protocol.PERIPHERAL_DAC
        break
    elif per == 3:
        per_msg = protocol.PERIPHERAL_MODBUS
        break
    elif per == 4:
        per_msg = protocol.PERIPHERAL_SYS
        break
    else:
        print ('Por favor, insira um valor valido!')

if per_msg == protocol.PERIPHERAL_GPIO and type_msg == protocol.TYPE_CONFIG:
    size = 2
    print ('Para configuracao de GPIO, o payload deve conter 2 bytes.')
else:
    size = int(input('Insira o tamanho do seu Payload: '))

i = 0
payl = list(())
while i < size:
    payl.append(int(input(f'Insira o termo {i+1} do seu payload ')))
    i+=1

payload = bytearray(payl)

print('Start: ', protocol.START)
print('Type: ', type_msg)
print('Peripheral: ', per_msg)
print('Size: ', size)
print('payload: ', payload)