# Crie um programa que calcule a soma entre todos os números ímpares que são multíplos de três que se encontram no intervalo de 1 até 500.

soma = 0
for numero in range(1, 501):
    if numero % 2 == 1 and numero % 3 == 0:
        soma += numero
print(f'A soma dos números ímpares multiplos de 3 até 500 é:', soma)
