# Elabore um programa que calcule o valor a ser pago por um produto, considerando o seu preço normal e condição de pagamento:

# - À vista dinheiro / cheque: 10% de desconto
# - A vista no cartão: 5% de desconto
# - em até 2x no cartão: preço normal
# - 3x ou mais no cartão: 20% de juros

valor_produto = float(input('Digite o valor do produto: '))
print("""
[ 1 ] À vista dinheiro / cheque: 10% de desconto
[ 2 ] À vista no cartão: 5% de desconto
[ 3 ] Em até 2x no cartão: preço normal
[ 4 ] 3x ou mais no cartão: 20% de juros
""")

opcao = int(input('Escolha a forma de pagamento (1 - 4): '))
if opcao == 1:
    valor_final = valor_produto - (valor_produto * 0.10)
elif opcao == 2:
    valor_final = valor_produto - (valor_produto * 0.05)
elif opcao == 3:
    valor_final = valor_produto
elif opcao == 4:
    parcelas = int(input('Quantas parcelas? '))
    valor_final = valor_produto + (valor_produto * 0.20)
    print(f'Sua compra será parcelada em {parcelas}x de R${valor_final / parcelas:.2f}')
else:
    print('Opção Inválida!')
    valor_final = None
if valor_final is not None:
    print(f'Valor final a pagar: R${valor_final:.2f}')
