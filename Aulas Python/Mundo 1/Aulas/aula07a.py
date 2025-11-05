# Aula sobre Operadores Aritméticos

# + - Soma
# - - Subtração
# * - Multiplicação
# / - Divisão
# ** - Potencia
# // - Divisão Inteira
# % - Resto da divisão

# 5 + 2 == 7
# 5 - 2 == 3
# 5 * 2 == 10
# 5 / 2 == 2.5
# 5 ** 2 == 25
# 5 // 2 == 2
# 5 % 2 == 1

# Ordem de Precedência

# 1- ()
# 2- **
# 3- *, /, //, %
# 4- +, -

# EXEMPLOS

# 5 + 3 * 2 == 11
# 3 * 5 + 4 ** 2 == 31
# 3 * ( 5 + 4 ) ** 2 == 243

n1 = int(input('Um valor: '))
n2 = int(input('Outro valor: '))
s = n1 + n2
m = n1 * n2
d = n1 / n2
di = n1 // n2
p = n1 ** n2
print('A soma é {}, o produto é {}, a divisão é {}, a divisão inteira é {:.2f} e a potência {}'.format(s, m, d, di, p))
