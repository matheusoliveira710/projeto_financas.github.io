print(
"""Crie um programa que leia o nome e o preço de vários produtos. O programa deverá perguntar se o usuário vai continuar. No final, mostre:

A) Qual é o total gasto na compra

B) Quantos produtos custam mais de R$1.000,00

C) Qual o nome do produto mais barato
"""
)
total_compra = 0
produtos_caros = 0
nome_mais_barato = ""
preco_mais_barato = float("inf")
continuar = "S"

print("=" * 50)
print("           SISTEMA DE COMPRAS")
print("=" * 50)
while continuar == "S":
    nome_produto = str(input("Digite o nome do produto: ")).strip()
    preco_produto = float(input('Digite o valor do produto: R$'))

    total_compra += preco_produto

    if preco_produto > 1000:
        produtos_caros += 1

    if preco_produto < preco_mais_barato:
        preco_mais_barato = preco_produto
        nome_mais_barato = nome_produto

    continuar = input("Deseja continuar? [S/N] ").strip().upper()
    while continuar not in ["S", "N"]:
        print("Opção inválida! Digite S para SIM ou N para NÃO.")
        continuar = input("Deseja continuar? [S/N] ").strip().upper()

print("\n" + "=" * 50)
print("           RESUMO DA COMPRA")
print("=" * 50)
print(f"A) Total gasto na compra: R${total_compra:.2f}")
print(f"B) Produtos que custam mais de R$ 1.000,00: {produtos_caros}")
print(f"C) Produto mais barato: {nome_mais_barato} (R${preco_mais_barato:.2f})")
print("=" * 50)
