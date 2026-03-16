def to_hex(value: int) -> str:
    '''Converte CRC para string hexadecimal.'''
    return hex(value)

def to_bytes(value: int) -> bytes:
    '''Converte CRC para dois bytes.'''
    return value.to_bytes(2, "big")