# Escreva um programa que leia a velocidade de um carro. Se ele ultrapassar 80Km/h, mostre uma mensagem dizendo que ele foi multado. A multa vai custar R$7,00 por Km acima do limite

vel = float(input('Digite a velocidade marcada no velocímetro: '))

if vel > 80:
    print('Você foi multado!')
    multa = (vel - 80) * 7
    print(f'O valor da multa é de R${multa:.2f}')
