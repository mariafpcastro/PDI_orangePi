import protocol

dados = 'AA 01 01 02 0A 00 34 74'

check = protocol.check_packet(dados)

if check == 1:
    print("Checksum OK, analisando dados...")
    protocol.parse_packet(dados)
else:
    print ("Algo deu errado!")
