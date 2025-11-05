# Faça um programa que leia o ano de nascimento de um jovem e informe, de acordo com sua idade:

# Se ele ainda vai se alistar ao serviço militar
# Se é a hora de se alistar
# Se já passou do tempo de alistamento

# Seu programa também deverá mostrar o tempo que falta ou que passou do prazo de alistamento

from datetime import date

# Entrada: ano de nascimento
ano_nascimento = int(input("Ano de nascimento: "))
ano_atual = date.today().year

# Cálculo da idade
idade = ano_atual - ano_nascimento

print(f"Quem nasceu em {ano_nascimento} tem {idade} anos em {ano_atual}.")

# Regras de alistamento
if idade < 18:
    faltam = 18 - idade
    ano_alistamento = ano_atual + faltam
    print(f"Ainda faltam {faltam} anos para o alistamento.")
    print(f"Seu alistamento será em {ano_alistamento}.")
elif idade == 18:
    print("Você deve se alistar \033[31mIMEDIATAMENTE\033[m!")
elif idade > 18 and idade < 60:
    passaram = idade - 18
    ano_alistamento = ano_atual - passaram
    print(f"Você já deveria ter se alistado há {passaram} anos.")
    print(f"Seu alistamento foi em {ano_alistamento}.")
else:
    print("Não é mais necessário se alistar (idade acima do limite).")
