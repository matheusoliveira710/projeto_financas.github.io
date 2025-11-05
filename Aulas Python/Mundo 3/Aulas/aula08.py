# import módulo, vai importar todas as bibliotecas existentes no módulo
# from modulo import x - vai importar somente o que for selecionado
# math - biblioteca de matemática
# módulo ceil: Faz arredondamento para cima
# módulo floor: Faz arredondamento para baixo
# módulo trunc: Vai eliminar qualquer número depois da vírgula
# módulo pow: Faz cálculo de potência ou exponenciação
# módulo sqrt: Faz cálculo de raiz quadrada
# módulo factorial: Faz cálculo de fatorial

from math import sqrt, floor
print('====' * 10)
x = float(input('Digite um número: '))
print('====' * 10)
raiz = sqrt(x)
print('A raiz de {:.0f} é {:.2f}'.format(x, floor(raiz)))

print('====' * 10)
num1 = int(input('Digite o primeiro valor: '))
print('====' * 10)
num2 = int(input('Digite o segundo valor: '))
print('====' * 10)
s = num1 + num2
sub = num1 - num2
m = num1 * num2
d = num1 / num2
di = num1 // num2
e = num1 ** num2
print(f'A soma entre {num1} e {num2}, corresponde ao valor {s}.')
print('====' * 10)
print(f'A subtração entre {num1} e {num2}, corresponde ao valor {sub}.')
print('====' * 10)
print(f'A multiplicação entre {num1} e {num2}, corresponde ao valor {m}.')
print('====' * 10)
print(f'A divisão entre {num1} e {num2}, corresponde ao valor {d}.')
print('====' * 10)
print(f'A divisão inteira entre {num1} e {num2}, corresponde ao valor {di}.')
print('====' * 10)
print(f'A exponenciação entre {num1} e {num2}, corresponde ao valor {e}.')
print('====' * 10)
print('Programa Finalizado!')
