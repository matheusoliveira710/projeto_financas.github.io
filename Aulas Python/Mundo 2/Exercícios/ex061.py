# Refaça o desafio 051, lendo o primeiro termo e a razão de uma PA, mostrando os 10 primeiros termos da progressão usando a estrutura while.

primeiro = int(input('Digite o primeiro termo da PA: '))
razao = int(input('Digite a razão da PA: '))

print('\nOs 10 primeiros termos da PA são: ')

contador = 0

while contador < 10:
    termo = primeiro + contador * razao
    print(termo, end=" --> ")
    contador += 1
print('Fim!')
