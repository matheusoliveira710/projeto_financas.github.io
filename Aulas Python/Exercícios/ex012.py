# Faça um programa que leia o preço de um produto e mostre seu novo preço, com 5% de desconto.
preco = float(input('Digite o valor do produto: R$'))
print(f'O valor do preço corresponde a R${preco:.2f}')
preco_novo = preco - 5
print(f'O preço antigo do produto era de R${preco:.2f}, e com 5% de desconto, vai para R${preco_novo:.2f}.')
