# Faça um programa que jogue par ou impar com o computador. O jogo só será interrompido quando o jogador perder, mostrando o total de vitórias consecutivas que ele conquistou no fim do jogo.

import random

vitorias = 0
while True:
    jogador = int(input('Digite um número: '))
    escolha = input('Par ou Impar? [P/I] ')
    computador = random.randint(0, 10)
    total = jogador + computador
    if (total % 2 == 0 and escolha == "P") or (total % 2 == 1 and escolha == "I"):
        vitorias += 1
        print(f"você jogou {jogador} e o computador {computador}. Total {total}, você venceu!")
    else:
        print(f"você jogou {jogador} e o computador {computador}. Total {total}, você perdeu!")
        break
print(f"vitórias consecutivas: {vitorias}")
