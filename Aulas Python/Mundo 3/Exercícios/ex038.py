# Escreva um programa que leia dois números inteiros e compare-os, mostrando na tela uma mensagem:

# O primeiro valor é maior

# O segundo valor é maior

# Ambos são iguais

num1 = int(input('Digite um número: '))
num2 = int(input('Digite mais um número: '))

if num1 > num2:
    print(f'O valor {num1} é maior que o valor {num2}')
elif num1 < num2 :
    print(f'O valor {num1} é menor do que o valor {num2}')
else:
    print(f'O valor {num1} e o valor {num2} são iguais')
