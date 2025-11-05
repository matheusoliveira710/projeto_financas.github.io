# Aula sobre Condições:

# se carro.esquerda():          |       if carro.esquerda():
#   bloco _V_                   |           bloco True
# se não:                       |       else:
#   bloco _F_                   |           bloco False

# Condição
# if carro.esquerda():
#     bloco True
# else:
#     bloco False

# tempo = int(input('Quantos anos tem seu carro? '))
# if tempo <= 3:
#    print('Carro novo')
# else:
#    print('Carro velho')
#

#nome = str(input('Digite seu nome: '))
#if nome == 'Matheus':
#    print('Fala ai Matheus!')
#print(f'Bom dia, {nome}!')

n1 = float(input('Digite a primeira nota: '))
n2 = float(input('Digite a segunda nota: '))
m = (n1 + n2) / 2
print(f'A sua média foi {m:.1f}!')
if m >= 6:
    print('Parabéns, você foi aprovado!')
else:
    print('Boa sorte na próxima, você tá reprovado!')
