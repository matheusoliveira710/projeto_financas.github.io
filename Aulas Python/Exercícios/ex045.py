# Crie um programa que faça o computador jogar Jokenpô com você.
import random
import time

print('=== JOKENPÔ ===')
print('Escolha uma opção: ')
print('[ 1 ] Pedra')
print('[ 2 ] Papel')
print('[ 3 ] Tesoura')

jogador = int(input('Qual a sua jogada? '))
opcoes = ['Pedra', 'Papel', 'Tesoura']
computador = random.randint(0, 2)
print(f'Você escolheu: {opcoes[jogador - 1]}')
# print(f'Computador escolheu: {opcoes[computador - 1]}')
print('Jo')
time.sleep(0.85)
print('Ken')
time.sleep(0.85)
print('Pô!')
if jogador == computador:
    print('Empate!')
elif (jogador == 1 and computador == 3) or \
     (jogador == 2 and computador == 1) or \
     (jogador == 3 and computador == 2):
     print('Você ganhou!')
else:
    print('Você perdeu!')
