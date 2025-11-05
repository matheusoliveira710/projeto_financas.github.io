# Faça um programa que leia um número inteiro e diga se ele é ou não um número primo.

num = int(input('Digite um número inteiro: '))

divisores = 0 # contador de divisores

for i in range(1, num + 1):
    if num % i == 0:
        divisores += 1

if divisores == 2: #só pode ter dois divisores (1 e ele mesmo)
    print(f"{num} é um número primo")
else:
    print(f"{num} NÃO é um número primo")
