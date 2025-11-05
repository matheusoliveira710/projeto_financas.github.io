# Escreva um programa que leia um número n inteiro qualquer e mostre na tela os n primeiros elementos de Sequência de fibonacci.

n = int(input('Quantos termos da sequencia de Fibonnaci você quer escrever? '))
print('\nOs {n} primeiros números da sequencia de Fibonnaci são: ')

termo1 = 0
termo2 = 1
contador = 0

while contador < n:
    if contador == 0:
        print('0', end="")
    elif contador == 1:
        print('--> 1', end="")
    else:
        proximo = termo1 + termo2
        print(f' → {proximo}', end='')
        termo1 = termo2
        termo2 = proximo

    contador += 1
