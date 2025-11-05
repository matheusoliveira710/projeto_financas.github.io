# Crie um programa que leia duas notas de um aluno e calcule a sua média, mostrando uma mensagem no final, de acordo com a média atingida:

# - Média abaixo de 5.0: Reprovado
# - Média entre 5.0 e 6.9: Recuperação
# - Média acima de 7: Aprovado!

nota1 = float(input('Digite sua primeira nota: '))
nota2 = float(input('Digite sua segunda nota: '))
media = (nota1 + nota2) / 2
if media >= 7:
    print(f'A média foi de \033[32m{media:.0f}\033[m')
    print('\033[32mAprovado\033[m!')
elif media <= 5:
    print(f'A média foi de \033[31m{media:.0f}\033[m')
    print('\033[31mReprovado\033[m!')
elif media > 5 and media < 7:
    print(f'A média foi de \033[33m{media:.0f}\033[m')
    print('\033[33mRecuperação\033[m!')
