# Faça um programa que leia o nome completo de uma pessoa, mostrando em seguida, o primeiro nome e o ultimo separadamente.
# ex: Ana Maria de Souza
# primeiro: Ana
# Ultimo: Souza

nome_completo = input('Digite seu nome completo: ').strip()
partes = nome_completo.split()
primeiro_nome = partes[0]
ultimo_nome = partes[-1]
print(f'Primeiro nome: {primeiro_nome}')
print(f'Ultimo nome: {ultimo_nome}')
