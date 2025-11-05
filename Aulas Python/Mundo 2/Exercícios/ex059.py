# Crie um programa que leia dois valores, e mostre um menu na tela:

# [ 1 ] somar
# [ 2 ] multiplicar
# [ 3 ] maior
# [ 4 ] novos números
# [ 5 ] sair
# Seu programa deverá realizar a operação solicitada em cada caso.
import time

n1 = float(input('Digite o primeiro valor: '))
n2 = float(input('Digite o segundo valor: '))

opcao = 0

while opcao != 5:
    print('\n' + '='*20)
    print('MENU DE OPÇÕES')
    print('='*20)
    print('[ 1 ] Somar')
    print('[ 2 ] Multiplicar')
    print('[ 3 ] Maior')
    print('[ 4 ] Novos números')
    print('[ 5 ] Sair do programa')
    print('='*20)

    opcao = int(input('Escolha uma opção: '))
    
    if opcao == 1:
        resultado = n1 + n2
        print(f'\nA soma de {n1} + {n2} = {resultado}')
    
    elif opcao == 2:
        resultado = n1 * n2
        print(f'\nA multiplicação de {n1} × {n2} = {resultado}')
    
    elif opcao == 3:
        if n1 > n2:
            print(f'\nO maior número é: {n1}')
        elif n2 > n1:
            print(f'\nO maior número é: {n2}')
        else:
            print(f'\nOs números são iguais: {n1}')
    
    elif opcao == 4:
        print('\nDigite novos números:')
        n1 = float(input('Primeiro valor: '))
        n2 = float(input('Segundo valor: '))
        print('Números atualizados com sucesso!')

    elif opcao == 5:
        time.sleep(1.5)
        print('\nSaindo do programa... Até logo!')
    
    else:
        print('\nOpção inválida! Digite um número entre 1 e 5.')
    
print('Programa encerrado!')
