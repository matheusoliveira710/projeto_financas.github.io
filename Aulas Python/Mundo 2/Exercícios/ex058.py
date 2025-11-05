# Melhore o jogo do desafio028, onde o computador vai pensar em um número entre 0 e 10. Só que agora, o jogador vai tentar adivinhar até acertar, mostrando no final, quantos palpites foram necessários para vencer.
import random
import time

numero = random.randint(1, 10)
palpites = 0

while True:
    num = int(input('Digite um valor entre 0 e 10: '))
    palpites += 1

    print('---' * 5)
    print('Pensando...')
    time.sleep(1)
    print('---' * 5)

    if num == numero:
        print('PARABÉNS! Você acertou!')
        print(f'O número que eu pensei foi realmente {numero}!')
        print(f'Você precisou de {palpites} palpites para vencer!')
        break
    else:
        print('Você errou! Tente novamente.')
        print('----' * 10)

print('Fim do jogo! Obrigado por jogar!')
