from datetime import date

# Faça um programa que leia um ano qualquer e mostre se ele é ano Bissexto
print('Que ano quer analisar? Coloque 0 para analisar o ano atual: ')
ano = int(input('Digite um ano: '))
if ano == 0:
    ano = date.today().year
if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
    print(f'O ano {ano} é bissexto!')
else:
    print(f'O ano {ano} não é bissexto!')
