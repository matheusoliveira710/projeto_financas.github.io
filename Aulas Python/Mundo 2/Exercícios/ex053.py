# Crie um programa que leia uma frase qualquer e diga se ela é um palíndromo, desconsiderando os espaços.

frase = input('Digite uma frase: ').strip().lower()

frase_sem_espaco = frase.replace(" ", "")

if frase_sem_espaco == frase_sem_espaco[::-1]:
    print('É um palíndromo!')
else:
    print('Não é um palíndromo!')
