# Crie um programa que leia um número real qualquer pelo teclado e mostre na tela, a sua porção inteira.
# Digite um número: 6,127
# O número 6,127 tem a parte inteira 6.

num = float(input('Digite um valor: '))
print('O valor digitado foi {}, porém a sua parte inteira é {}'.format(num, int(num)))
