# Crie um programa que leia quanto de dinheiro uma pessoa tem na carteira, e mostre quantos dólares ela pode comprar.

valor_cart = int(input('Quanto de dinheiro você tem na carteira? R$'))
dolar = 5.56

posse = valor_cart / dolar

print(f'Com R${valor_cart:.0f} reais, você pode trocar por U$ {posse:.2f} dólares.')
