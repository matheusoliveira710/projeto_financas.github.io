# Desenvolva uma lógica que leia o peso de uma pessoa, calcule o seu IMC e mostre seu status de acordo com a tabela abaixo:

# - Abaixo de 18.5: Abaixo do Peso
# - Entre 18 e 25: Peso ideal
# - Entre 25 até 30: Sobrepeso
# - Entre 30 até 40: Obesidade
# - Acima dos 40: Obesidade Mórbida


peso = float(input('Digite o seu peso (kg): '))
altura = float(input('Digite sua altura (m): '))
imc = peso / (altura ** 2)
print(f'Seu IMC é: {imc:.2f}')
if imc < 18.5:
    print('Abaixo do peso')
elif imc <= 25:
    print('Peso Ideal')
elif imc <= 30:
    print('Sobrepeso')
elif imc <= 40:
    print('Obesidade')
else:
    print('Obesidade Mórbida')
