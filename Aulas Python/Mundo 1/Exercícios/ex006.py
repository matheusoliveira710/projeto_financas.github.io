# Crie um algoritmo que leia um número e mostre seu dobro, seu triplo e a sua raiz quadrada e mostre na tela
from math import sqrt
n = int(input('Digite um valor: '))
raiz = sqrt(n)
dobro = n * 2
tri = n * 3
print('O valor digitado foi {:.0f}, o dobro do número {:.0f} equivale ao seguinte valor {:.0f}, e o triplo do valor {:.0f}, equivale ao valor: {:.0f}.'.format(n, n, dobro, n, tri))
