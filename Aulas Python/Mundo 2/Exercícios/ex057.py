# Faça um programa que leia o sexo de uma pessoa, mas só aceite os valores 'M' e 'F'. Caso esteja errado, peça a digitação novamente até ter um valor correto.

"""sexo = str(input('Digite seu sexo (M para Masculino / F para Feminino): ')).strip().upper()[0]

while sexo != 'M' and sexo != 'F':
    print('Opção inválida! Por favor, digite apenas M ou F.')
    sexo = str(input('Digite seu sexo (M para Masculino / F para Feminino): ')).strip().upper()[0]

print(f'Sexo registrado: {"Masculino" if sexo == "M" else "Feminino"}')"""

s = str(input('Digite seu sexo (M pra Masculino / F pra Feminino): ')).strip().upper()
while s != 'M' and s != 'F':
    print('Opção inválida! Por favor, digite apenas M ou F.')
    s = str(input('Digite seu sexo (M pra Masculino / F pra Feminino): ')).strip().upper()
print(f'Sexo registrado: {"Masculino" if s == "M" else "Feminino"}')
