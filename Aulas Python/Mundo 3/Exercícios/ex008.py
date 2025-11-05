# Escreva um programa que leia um valor em metros e o exiba convertido em centímetros e milímetros.

n = float(input('Digite um valor em metros: '))
c = n * 100
m = n * 1000
print('O valor em metros corresponde a: {:.0f} metros.'.format(n))
print('O valor com {:.0f} metros, corresponde a {:.0f} centímetros'.format(n, c))
print('O valor com {:.0f} metros, corresponde a {:.0f} milímetros'.format(n, m))
