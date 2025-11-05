# Desenvolva um programa que pergunte a distância de uma viagem em Km. Calcule o preço da passagem, cobrando R$0,50 por km para viagens de até 200km, e R$0,45 para viagens mais longas.

distancia = int(input('Qual é a distância da viagem? '))
if distancia >= 200:
    print(f'A distância é de {distancia} Km.')
    preco = distancia * 0.45
    print(f'O preço da passagem é de R${preco:.2f} reais!')
else:
    print(f'A distância é de {distancia} Km.')
    preco = distancia * 0.50
    print(f'O preço da passagem é de R${preco:.2f} reais!')
