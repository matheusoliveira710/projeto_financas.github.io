# Aula sobre Condições parte 1:

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
print('A sua média foi {:.1f}!'.format(m))
if m >= 6:
    print('Parabéns, você foi \033[1;32maprovado\033[m!')
else:
    print('Boa sorte na próxima, você tá \033[1;31mreprovado\033[m!')
