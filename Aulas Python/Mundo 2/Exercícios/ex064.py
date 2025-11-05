# Crie um programa que leia vários números inteiros pelo teclado.
# O programa só vai parar quando o usuário digitar 999, que é a condição de parada.
# No final, mostre quantos números foram digitados, e qual a soma entre eles

numero = 0
contador = 0
soma = 0
while numero != 999:
    numero = int(input('Digite um valor (999) para parar: '))
    if numero != 999:
        contador += 1
        soma += numero
    print('=' * 38)
print(f'Você digitou {contador} números e a soma deles foi {soma}')
print('=' * 46)
print('Fim!')
print('=' * 4)
