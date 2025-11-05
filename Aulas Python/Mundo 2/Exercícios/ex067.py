# Faça um programa que mostre a tabuada de vários números, um de cada vez, para cada valor digitado pelo usuário. O programa deverá ser interrompido quando o número solicitado for negativo.

while True:
    num = int((input('Digite um número para ver a sua tabuada (negativo para parar): ')))

    if num < 0:
        break
    print(f"\nTabuada do {num}: ")
    for c in range(1, 11):
        print(f'{num} x {c} = {num * c}')
    print()
print("Programa encerrado!")
