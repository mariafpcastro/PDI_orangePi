import mathematicsLib as math


print ("Este codigo foi feito para que seja calculado um lado do triangulo de pitagoras!")
print ("primeiro, escolha qual das opcoes voce quer calcular:")
while(1):
	print ("1. Cateto")
	print ("2. Hipotenusa")
	opt = int(input (">"))
	if opt  == 2:
		calc = "hip"
		a = int(input ("Digite o valor do cateto a: "))
		b = int(input ("Digite o valor do cateto b: "))
		break
	elif opt == 1:
		calc = "cat"
		while (1):
			a = int(input ("Digite o valor da hipotenusa: "))
			b = int(input ("Digite o valor do cateto conhecido: "))
			if a <= b:
				print ("Ops, valores invalidos! A hipotenusa e sempre maior que o cateto. Tente novamente!")
			else:
				break
		break
	else:
		print ("Opcao invalida! Escolha apenas entre as opcoes abaixo:")

result = math.Pitagoras(a, b, calc)
print(result)
