# Faça um programa que leia a altura e a largura de uma parede em metros, calcule a sua área e a quantidade de tinta necessária para pintá-la, sabendo que cada litro de tinta, pinta uma área de 2m².
altura = int(input('Digite a altura da parede em metros: '))
base = int(input('Digite a largura da parede em metros: '))
area = altura * base
tinta_necessaria = area / 2

print(f'A altura da parede é: {altura} metros')
print(f'A largura da parede é: {base} metros')
print(f'A área total da parede é: {area} metros')
print(f'Você precisará de {tinta_necessaria:.0f} litros para pintar a parede com {altura} metros de altura e {base} metros de largura.')
