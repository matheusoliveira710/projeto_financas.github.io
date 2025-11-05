# Crie um programa que leia o nome de uma pessoa e diga se ela tem "Silva" no nome.

nome = input('Digite seu nome: ')

tem_silva = "silva" in nome.lower()

if tem_silva:
    print('Seu nome tem Silva.')
else:
    print('Seu nome não tem Silva')
