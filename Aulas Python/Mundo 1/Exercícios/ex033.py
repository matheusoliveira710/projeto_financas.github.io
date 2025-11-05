# Faça um programa que leia três números e mostre qual é o maior e qual é o menor

print('----' * 8)
n1 = int(input('Digite um valor: '))
print('----' * 8)
n2 = int(input('Digite outro valor: '))
print('----' * 8)
n3 = int(input('Digite mais um valor: '))
print('----' * 8)

menor = min(n1, n2, n3)
maior = max(n1, n2, n3)

print(f'O maior número é {maior}!')
print('----' * 8)
print(f'O menor número é {menor}!')
print('----' * 8)