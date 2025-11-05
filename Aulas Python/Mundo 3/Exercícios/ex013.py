# Faça um algoritmo que leia o salário de um funcionário e mostre seu novo salário, com 15% de aumento
print('----' * 10)
salario = float(input('Digite o valor do seu salário: R$'))
valor_aumento = salario * 0.15
novo_salario = salario + valor_aumento
print('----' * 19)
print(f'O seu salário era de R${salario:.2f}, mais com 15% de aumento, vai para R${novo_salario:.2f}.')
