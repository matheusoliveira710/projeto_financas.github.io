# Interpretação normal
import time

# laço c no intervalo(0,3)
    #se moeda
        #pega
    #passo
    #pula
#passo
#pega

# Interpretação via Python

# for c in range(0,3):
    #if moeda
        #pega
    #passo
    #pula
#passo
#pega

#i = int(input('Início: '))
#f = int(input('Fim: '))
#p = int(input('Passo: '))
#for c in range(i, f+1, p):
#    print(c)
#print('FIM!')

s = 0
for c in range(0, 4):
    n = int(input('Digite um número: '))
    s += n
print(f'O somatório de todos os valores é {s}.')
