# Escreva um programa que faça o computador "pensar" em um numero inteiro entre 0 e 5 e peça para o usuário tentar descobrir qual foi o número escolhido pelo computador. O programa deverá escrever na tela se o usuário venceu ou perdeu.

import random
import time

print('Vou escolher um número entre 0 e 5, tente adivinhar, boa sorte!')
print('----' * 10)
num = int(input('Digite um número entre 0 e 5: '))
print('----' * 10)
numero = random.randint(0,5)
time.sleep(2)
print('Pensando...')
time.sleep(2)
print('----' * 5)
print('E o resultado é...')
time.sleep(2)
print('----' * 5)
if num == numero:
    print('Você acertou, parabéns!')
else:
    print('Você errou, boa sorte na próxima!')
