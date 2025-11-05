# Crie um programa que leia o nome completo de uma pessoa e mostre

# - O nome com todas as letras maiúsculas

# - O nome com todas as letras maiúsculas

# - Quantas letras totais (sem considerar espaços)

# - Quantas letras tem o primeiro nome

# Solicita o nome completo do usuário
nome_completo = input("Digite seu nome completo: ").strip()

# Nome com todas as letras maiúsculas
print("Nome em maiúsculas:", nome_completo.upper())

# Nome com todas as letras minúsculas
print("Nome em minúsculas:", nome_completo.lower())

# Quantidade de letras sem considerar os espaços
total_letras = len(nome_completo.replace(" ", ""))
print("Total de letras (sem espaços):", total_letras)

# Quantidade de letras do primeiro nome
primeiro_nome = nome_completo.split()[0]
print("Letras no primeiro nome:", len(primeiro_nome))
