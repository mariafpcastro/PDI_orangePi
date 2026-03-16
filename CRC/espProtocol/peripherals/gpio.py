import protocol as pc
import utils

def gpio_read(type, payload):

    pino = int(payload[0], 16)

    if type == pc.TYPE_CONFIG or type == pc.TYPE_EVENT or type == pc.TYPE_WRITE:
        if payload[1] == pc.STATUS_OK:
            print ("Sucesso ao configurar GPIO ", pino)
        elif payload[1] == pc.STATUS_FAIL:
            print("Erro de configuracao do GPIO ", pino)
        else:
            print("Nao sei!")
    elif type == pc.TYPE_READ:
        if payload[1] == '01':
            print(f'GPIO {pino} em nivel logico HIGH')
        elif payload[1] == '00':
            print(f'GPIO {pino} em nivel logico LOW')
        else:
            print('Nao sei!')