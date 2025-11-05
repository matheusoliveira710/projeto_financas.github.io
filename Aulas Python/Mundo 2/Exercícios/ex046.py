# Faça um programa que mostre na tela uma contagem regressiva para o estouro de fogos de artifício, indo de 10 a 0, com uma pausa de 1 segundo entre eles.

import time

n = 10
for c in range(n, 0, -1):
    print(c)
    time.sleep(1.5)
print('Fim!')
