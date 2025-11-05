# Faça um programa que leia uma frase pelo teclado e mostre:

# Quantas vezes a letra A aparece.

# Em que posição ela aparece a primeira vez.

# Em que posição ela aparece pela última vez.

frase = input('Digite uma frase: ')
quant = frase.count('a')
primeira_posicao = frase.find('a')
ultima_posicao = frase.rfind('a')
print(f'A letra "A" aparece {quant} vezes na frase.')
print(f'A primeira letra "A" aparece na posição {primeira_posicao}.')
print(f'A ultima letra "A" aparece na posição {ultima_posicao}.')
