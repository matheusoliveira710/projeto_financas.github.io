# Aula sobre Fatiamento de Strings (Cadeia de Texto ou caracteres)

frase = 'Curso em Vídeo Python'
#print(frase[:5])
#print(frase[9])
#print(frase.count('o', 0, 14))

# Transformação:
# print(frase.capitalize()) - retorna uma cópia da string com o primeiro caractere em maiúsculo e o resto em minúsculo
print(frase.capitalize())
# print(frase.lower()) - Vai jogar toda a frase pra minúsculo
print(frase.lower())
# print(frase.upper()) - Vai jogar toda a frase pra maiúsculo
print(frase.upper())
# print(frase.title()) - Vai pegar a inicial de cada frase e botar pra maiúsculo
print(frase.title())
# print(frase.strip()) - Tira todos os espaços
print(frase.strip())
# print(frase.rstrip()) - Tira todos os espaços da direita
print(frase.rstrip())
# print(frase.lstrip()) - Tira todos os espaços da esquerda
print(frase.lstrip())

# Divisão
# print(frase.split()) - Faz um array (lista)
print(frase.split())

# Junção

print('-'.join(frase.split()))
