# Desenvolva um programa que leia seis números inteiros e mostre na tela a soma apenas daqueles que forem pares. Se o valor digitado for ímpar, desconsidere.

soma = 0 # acumulador da soma

for i in range(1, 7): 
    numero = int(input(f'Digite o {i}º número inteiro: '))
    if numero % 2 == 0:
        soma += numero
print(f"\n A soma dos números pares digitados é: {soma}")
