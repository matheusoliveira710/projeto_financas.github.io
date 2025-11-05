# Desenvolva um programa que leia o comprimento de 3 retas e diga se ao usuário se elas podem ou não formar um triângulo
print('Digite o comprimento dos 3 segmentos de reta:')
c1 = float(input('Primeiro triangulo: '))
c2 = float(input('Segundo triangulo: '))
c3 = float(input('Terceiro triangulo: '))

if c1 < c2 + c3 and c2 < c1 + c3 and c3 < c1 + c2:
    print('Os segmentos \033[0;32mpodem\033[0m formar um triângulo!')
else:
    print('Os segmentos \033[0;31mNÃO\033[0m podem formar um triângulo.')
