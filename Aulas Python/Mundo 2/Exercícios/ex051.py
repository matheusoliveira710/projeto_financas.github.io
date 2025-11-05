# Desenvolva um programa que leia o primeiro termo e a razão de uma PA. No final, mostre os 10 primeiros termos dessa progressão.

# Primeiro termo: 3
# Razão: 2

primeiro = int(input('Digite o primeiro termo da PA: '))
razao = int(input('Digite a razão da PA: '))

print("\nOs 10 primeiros termos da PA são: ")
for i in range(10):
    termo = primeiro + i * razao
    print(termo, end=" --> ")

print('FIM!')
