# Escreva um programa para aprovar o empréstimo bancário para a compra de uma casa. O programa vai perguntar o valor da casa, o salário do comprador e em quantos anos ele vai pagar. Calcule a prestação mensal, sabendo que ela não pode exceder os 30% do salario, ou então, o empréstimo será negado

valor_casa = float(input('Qual o valor da casa? R$'))
salario = float(input('Quanto você ganha de salário? R$'))
anos = int(input('Em quantos anos vai querer pagar? '))
total_parcelas = anos * 12
parcelas = valor_casa / total_parcelas
limite = salario * 0.30

print(f'Para pagar uma casa no valor de R${valor_casa:.2f} em {anos} anos, '
      f'a prestação será de R${parcelas:.2f}.')

if parcelas <= limite:
    print('\033[32mEmpréstimo Aprovado!\033[m')
else:
    print('\033[31mEmpréstimo Negado!\033[m')
