'import numpy as np'

def add(a: float, b: float):
    #Docstrings
    ''' Retorna o resultado de a mais b.'''
    return(a+b)

def subtract(a: float, b: float):
    #Docstrings
    '''Retorna o resultado de b menos a.'''
    return (a-b)

def multiply(a: float, b: float):
    #Docstrings
    '''Retorna o resultado de a vezes b'''
    return (a*b)

def divide (a: float,b: float):
    '''Retorna o resultado da divisão de a por b.'''
    return (a/b)

def potencia (a: float, b: float):
    #Docstrings
    '''Retorna 'a' elevado a 'b' '''
    return (a**b)

def raiz (a:float, b:float) -> float:
    #Docstrings
    '''Retorna a raiz de 'b' grau do valor 'a' '''
    return (round (a**(1/b), 4))
