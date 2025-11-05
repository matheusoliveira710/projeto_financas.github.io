n = s = 0
while True:
    n = int(input('Digite um número: '))
    if n == 999:
        break
    s += n
print(f'A soma vale: {s}')
"""
nome = 'José'
idade = 68
print(f'{nome} tem {idade} anos.') # PYTHON 3.6+
print('{} tem {} anos.'.format(nome, idade)) # PYTHON 3
print('%s tem %d anos.' % (nome, idade)) # PYTHON 2
"""
