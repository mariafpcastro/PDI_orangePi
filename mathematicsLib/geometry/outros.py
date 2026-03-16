import numpy as np

def Pitagoras(a, b, calc='hip') -> float:
	#Docstrings
	'''
	Calcula um dos lados de um triângulo retângulo.

	Equacao:
	__________
	* Para 'hip': c = sqrt (a² + b²)
	* Para 'cat': c= sqrt (max(a,b)²-min(a,b)²)

	Parametros:
	__________
	* a (float): Valor conhecido de um dos lados do triangulo retangulo,
	    podendo ser um cateto ou a hipotenusa.
	* b (float): Valor conhecido do segundo lado do triangulo retangulo,
	    podendo ser um cateto ou a hipotenusa.
	* calc ('hip', 'cat', default='hip'): Valor que deseja encontrar, sendo:
		- hip = hipotenusa
		- cat = cateto
	
	Retorna:
	__________
		float: o valor do cateto ou hipotenusa calculado
	'''
	if calc == 'hip':
		c = np.sqrt((a**2) + (b**2))
	elif calc == 'cat':
		c = np.sqrt((max(a,b)**2) - (min(a,b)**2))
	else:
		c = '''Ops, aparentemente voce inseriu um valor invalido para 'calc',
por favor, insira 'hip' para hipotenusa ou 'cat' para cateto!'''
	return c
	
def distancia_2d(x1:float, y1:float, x2:float, y2:float) -> float:
	#Docstring
	'''
	Calcula a distancia entre dois pontos no plano cartesiano.
	
	Para planos 3D, utilize a funcao distancia_3d
	
	Equacao: 
	__________
		d = sqrt((x2 - x1)² + (y2 - y1)²)

	
	Parametros:
	__________
	* x1 (float): Coordenada x do primeiro ponto;
	* y1 (float): Coordenada y do primeiro ponto;
	* x2 (float): Coordenada x do segundo ponto;
	* y2 (float): Coordenada y do segundo ponto;

	Retorna:
	__________
		float: A distância entre dois pontos.
	'''

	return (np.sqrt((x2 - x1)**2 + (y2 - y1)**2))

def distancia_3d(x1:float, y1:float, z1:float, x2:float, y2:float, z2:float) -> float:
	#Docstring
	'''
	Calcula a distancia entre dois pontos no plano 3D.
	
	Para planos 2D, utilize a funcao distancia_2d
	
	Equacao: 
	__________
		d = sqrt((x2 - x1)² + (y2 - y1)² + (z2 - z1)²)
	
	Parametros:
	__________
	* x1 (float): Coordenada x do primeiro ponto;
	* y1 (float): Coordenada y do primeiro ponto;
	* z1 (float): Coordenada z do primeiro ponto;
	* x2 (float): Coordenada x do segundo ponto;
	* y2 (float): Coordenada y do segundo ponto;
	* z2 (float): Coordenada z do segundo ponto;

	Retorna:
	__________
		float: A distância entre dois pontos.
	'''

	return (np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2))

def perimetro_retangulo(largura:float, altura:float):
	#Docstring
	'''
	Calcula o perimetro de um retangulo

	Equacao:
	__________
		p = 2*largura + 2*altura
	
	Parametros:
	__________
	* largura (float): largura do retangulo
	* altura (float): altura do retangulo

	Retorna:
	____
		float: O perimetro do retangulo
	'''

	return (2*largura + 2*altura)