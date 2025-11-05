# Escreva um programa que pergunte o salário de um funcionário e calcule o valor do seu aumento.
# Para salários acima de R$1250,00, calcule um aumento de 10%
# Para salários abaixo ou iguais, calcule um aumento de 15%

salario = float(input('Digite o salário do funcionário: R$'))
if salario > 1250:
    aumento = salario * 0.10
    novo = salario + aumento
else:
    aumento = salario * 0.15
    novo = salario + aumento
print(f'O aumento será de R${aumento:.2f}')
print(f'O novo salário será de R${novo:.2f}')
