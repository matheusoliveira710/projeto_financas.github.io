# Faça um programa que leia um número de 0 a 9999 e mostre na tela, cada um dos digitos separados.

# Ex: Digite um número: 1834

# unidade: 4, dezena: 3, centena: 8, milhar: 1

numero = int(input('Digite um número: '))
if 0 < numero < 9999:
    numero_str = f'{numero:0>4}'
    print(f'Unidade: {numero_str[3]}')
    print(f'Dezena: {numero_str[2]}')
    print(f'Centena: {numero_str[1]}')
    print(f'Milhar: {numero_str[0]}')
else:
    print('Número fora do intervalo permitido!')
