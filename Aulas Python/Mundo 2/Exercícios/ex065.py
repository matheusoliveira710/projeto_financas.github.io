# Crie um programa que leia vários números inteiros pelo teclado. No final da execução, mostre a média entre todos os valores, e qual foi o maior e o menor valores lidos.
# O programa deve perguntar ao usuário se ele quer continuar ou não digitar valores.

numeros = []
continuar = 'S'

print("=" * 18)
print("ANÁLISE DE NÚMEROS")
print("=" * 18)

while continuar.upper() == 'S':
    try:
        numero = int(input("Digite um número inteiro: "))
        numeros.append(numero)

        # Pergunta se o usuário quer continuar
        continuar = input("Deseja continuar? [S/N]: ").strip()

        # Valida a resposta usando while
        while continuar.upper() not in ['S', 'N']:
            print("Opção inválida! Digite S para SIM ou N para NÃO.")
            continuar = input("Deseja continuar? [S/N]: ").strip()

    except ValueError:
        print("Erro: Por favor, digite apenas números inteiros!")
        continuar = input("Deseja continuar? [S/N]: ").strip()

if len(numeros) > 0:

    soma = 0
    i = 0
    while i < len(numeros):
        soma += numeros[i]
        i += 1
    media = soma / len(numeros)

    maior = numeros[0]
    i = 1
    while i < len(numeros):
        if numeros[i] > maior:
            maior = numeros[i]
        i += 1

    menor = numeros[0]
    i = 1
    while i < len(numeros):
        if numeros[i] < menor:
            menor = numeros[i]
        i += 1

    print("\n" + "=" * 30)
    print("RESULTADOS:")
    print("=" * 30)
    print(f"Total de números digitados: {len(numeros)}")
    print("=" * 30)
    print(f"Média dos valores: {media:.2f}")
    print("=" * 30)
    print(f"Maior valor: {maior}")
    print("=" * 30)
    print(f"Menor valor: {menor}")
    print("=" * 30)
else:
    print("\nNenhum número foi digitado!")
