# Refaça o desafio 009, mostrando a tabuada de um número que o usuário escolher, só que agora utilizando o laço for.

numero = int(input('Digite um número para ver a sua tabuada: '))

print(f"\nTabuada do {numero}:")
print("---" * 4)
for i in range(1, 11):
    resultado = numero * i
    print(f"{numero} x {i} = {resultado}")
    print("---" * 4)
