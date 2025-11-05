# Faça um programa que leia o comprimento de um cateto oposto e do cateto adjacente de um triangulo retangulo, calcule e mostre o comprimento da hipotenusa

import math

# Leitura dos Catetos
cateto_oposto = float(input('Digite o comprimento do cateto oposto: '))
cateto_adjacente = float(input('Digite o cateto adjacente: '))

# Cálculo da hipotenusa usando math.hypot
hipotenusa = math.hypot(cateto_oposto, cateto_adjacente)

# Resultado
print(f"O comprimento da hipotenusa é: {hipotenusa:.0f}")
