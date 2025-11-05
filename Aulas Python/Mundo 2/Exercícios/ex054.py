# Crie um programa que leia o ano de nascimento de sete pessoas. No final, mostre quantas pessoas ainda não atingiram a maioridade e quantas já são maiores.

from datetime import date

ano_atual = date.today().year
maiores = 0
menores = 0

for i in range(1, 8):
    nascimento = int(input(f'Digite o ano de nascimento da {i}ª pessoa: '))
    idade = ano_atual - nascimento
    if idade >= 18:
        maiores += 1
    else:
        menores += 1
print(f"\nTotal de pessoas maiores de idade: {maiores}")
print(f"Total de pessoas menores de idade: {menores}")
