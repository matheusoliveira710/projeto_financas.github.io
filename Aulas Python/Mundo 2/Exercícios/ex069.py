# Crie um programa que leia a idade e o sexo de várias pessoas. A cada pessoa cadastrada, o programa deverá perguntar se o usuário quer continuar ou não. No final, mostre:

# A) Quantas pessoas são maiores de 18 anos

# B) Quantos homens foram cadastrados

# C) Quantas mulheres tem menos de 20 anos

maiores_18 = 0
homens_cadastrados = 0
mulheres_menores_20 = 0

print("=== CADASTRO DE PESSOAS ===")
while True:
    print("\n" + "-" * 15)
    idade = int(input("Digite a idade: "))
    sexo = input("Digite o sexo: [M/F] ").strip().upper()
    while sexo not in ["M", "F"]:
        print("Sexo Inválido! Digite M para masculino ou F para feminino.")
        sexo = input("Digite o sexo: [M/F] ").strip().upper()
    if idade > 18:
        maiores_18 += 1
    if sexo == "M":
        homens_cadastrados += 1
    elif sexo == "F":
        mulheres_menores_20 += 1
    continuar = input("Deseja continuar [S/N]: ").strip().upper()
    while continuar not in ['S', 'N']:
        print("Resposta inválida! Digite S para sim ou N para não.")
        continuar = input("Deseja cadastrar outra pessoa? (S/N): ").strip().upper()
    if continuar == 'N':
        break
print("\n" + "=" * 30)
print("RESULTADOS DO CADASTRO")
print("=" * 30)
print(f"A) Pessoas maiores de 18 anos: {maiores_18}")
print(f"B) Homens cadastrados: {homens_cadastrados}")
print(f"C) Mulheres com menos de 20 anos: {mulheres_menores_20}")
