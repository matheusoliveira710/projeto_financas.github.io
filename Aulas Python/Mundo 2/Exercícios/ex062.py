# Melhore o desafio 061, perguntando ao usuário se ele quer mostrar mais alguns termos. O programa encerra quando ele disser que quer mostrar 0 termos.

primeiro = int(input('Digite o primeiro termo da PA: '))
razao = int(input('Digite a razao da PA: '))

print('\nOs 10 primeiros termos da PA são: ')

contador = 0
total_termos = 10

while contador < total_termos:
    termo = primeiro + contador * razao
    print(termo, end=' --> ')
    contador += 1
print('FIM!')

mais_termos = int(input('\nQuantos termos você quer mostrar a mais? (0 para encerrar): '))

while mais_termos != 0:
    total_termos += mais_termos
    while contador < total_termos:
        termo = primeiro + contador * razao
        print(termo, end=' --> ')
        contador += 1
    print('FIM!')
    mais_termos = int(input('\nQuantos termos você quer mostrar a mais? (0 para encerrar): '))

print('Programa Encerrado!')
