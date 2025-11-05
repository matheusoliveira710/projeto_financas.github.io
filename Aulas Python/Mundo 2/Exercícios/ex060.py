# Faça um programa que leia um número qualquer e mostre o seu fatorial.
import math
from math import factorial
n = int(input('Digite um valor: '))
fat = math.factorial(n)
print(f'A fatorial do número {n}, corresponde ao {fat}')
