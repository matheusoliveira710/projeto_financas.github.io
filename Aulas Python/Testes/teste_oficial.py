# carro.siga()
#if carro.esquerda():
# BLOCO __V__ {
#   carro.siga()
#   carro.direita()
#   carro.siga()
#   carro.direita
#   carro.esquerda()
#   carro.siga()
#   carro.direita()
#   carro.siga()
# }
#else:
# BLOCO __F__ {
#   carro.siga()
#   carro.esquerda()
#   carro.siga()
#   carro.esquerda()
#   carro.siga()
#}
#carro.pare()
# Condição:
# if carro.esquerda():
#   bloco True
# else:
#   bloco False
print('=====' * 6)
tempo = int(input('Quantos anos tem seu carro? '))
print('=====' * 6)
print('Carro novo!' if tempo <=3 else 'Carro velho!')
print('=====' * 6)
