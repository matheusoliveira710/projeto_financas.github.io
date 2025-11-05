# Crie um programa que leia o nome de uma cidade e diga se ela começa com o nome "Santo"

cidade = input('Digite o nome da cidade: ').strip()

# Verifica se a cidade começa com "SANTO" e o que vem após a palavra "Santo"
if cidade.upper().startswith('SANTO') and len(cidade) > 5 and cidade[5] != ' ':
    print(f'A cidade de nome "{cidade}" não começa com o nome "SANTO".')
else:
    print(f'A cidade de nome "{cidade}" começa com o nome "SANTO".')
 