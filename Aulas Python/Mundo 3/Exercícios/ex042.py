# Refaça o exercício 35 dos triângulos, acrescentando o recurso de mostrar que tipo de triângulo será formado:

# - Equilátero: Todos os lados iguais
# - Isósceles: Dois lados iguais
# - Escaleno: Todos os lados diferentes

print('Digite o comprimento dos 3 segmentos de reta:')
c1 = float(input('Primeiro lado: '))
c2 = float(input('Segundo lado: '))
c3 = float(input('Terceiro lado: '))

if c1 < c2 + c3 and c2 < c1 + c3 and c3 < c1 + c2:
    if c1 == c2 == c3:
        print('Podem formar um triângulo EQUILÁTERO!')
    elif c1 == c2 or c1 == c3 or c2 == c3:
        print('Podem formar um triângulo ISÓSCELES!')
    else:
        print('Podem formar um triângulo ESCALENO!')
else:
    print('Os valores informados NÃO podem formar um triângulo.')
