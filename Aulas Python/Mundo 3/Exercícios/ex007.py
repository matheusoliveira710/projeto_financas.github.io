# Desenvolva um programa que leia as duas notas de um aluno, calcule e mostre a sua média.
print('=' * 10)
nota_1 = int(input('Digite a primeira nota: '))
print('=' * 10)
nota_2 = int(input('Digite a segunda nota: '))
print('=' * 10)
s = nota_1 + nota_2
m = s / 2

print(f'A primeira nota digitada foi {nota_1}, a segunda nota digitada foi {nota_2}')
print('=' * 10)
print(f'A soma da primeira nota: {nota_1}, e da segunda nota: {nota_2}, a soma das notas equivale a: {s}')
print('=' * 10)
print('A média das notas equivale a {:.0f}'.format(m))
print('=' * 10)