# Desenvolva um programa que leia o nome, idade e sexo de 4 pessoas. No final do programa, mostre:

# A média de idade do grupo
# Qual é o nome do homem mais velho
# Quantas mulheres têm menos de 20 anos

soma_idade = 0
homem_mais_velho = ""
idade_homem_mais_velho = 0
mulheres_menos_20 = 0

for i in range(1, 5):
    print(f"\n--- {i}ª Pessoa ---")
    nome = input("Nome: ").strip()
    idade = int(input("Idade: "))
    sexo = input("Sexo [M/F]: ").strip().upper()

    soma_idade += idade

    # Verifica homem mais velho
    if sexo == "M":
        if idade > idade_homem_mais_velho:
            idade_homem_mais_velho = idade
            homem_mais_velho = nome

    # Conta mulheres com menos de 20
    if sexo == "F" and idade < 20:
        mulheres_menos_20 += 1

# Cálculo da média
media_idade = soma_idade / 4

print("\n===== RESULTADOS =====")
print(f"A média de idade do grupo é: {media_idade:.1f} anos")
if homem_mais_velho:
    print(f"O homem mais velho é {homem_mais_velho} com {idade_homem_mais_velho} anos")
else:
    print("Não há homens no grupo.")
print(f"Quantidade de mulheres com menos de 20 anos: {mulheres_menos_20}")
