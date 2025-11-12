import google.generativeai as genai
import os
import requests
import json
from pydantic import EmailStr  # Vamos usar para validar o email

# --- 1. Configuração de Segurança e API ---

# --- Chaves colocadas direto para teste ---
API_KEY_GEMINI = "AIzaSyAS3FKdGlhcU4Rtaw1hYNn4kYYSDUyQYkg"  # Sua chave Gemini
API_SECRET_KEY = "&p#pX%7^@!^^^^8YgbF&kt5910n2AI4!"  # Sua X-API-Key

# Configura a chave do Gemini
genai.configure(api_key=API_KEY_GEMINI)

# Endereço da sua API que está rodando
API_URL = "http://127.0.0.1:8000"

# Headers para a X-API-Key (usado para login/registro)
API_KEY_HEADERS = {
    "X-API-Key": API_SECRET_KEY,
    "Content-Type": "application/json"
}

# --- NOVO: "Memória" do Chatbot ---
# Aqui é onde vamos guardar o "crachá" (Token JWT) do usuário após o login.
USER_AUTH_TOKEN = None


# --- 2. Definição das Ferramentas (Agora com Login) ---

def register_user(email: EmailStr, password: str):
    """
    Registra um novo usuário no sistema financeiro.
    """
    print(f"\n[Debug] 🤖 Gemini decidiu chamar: register_user(email='{email}')")
    print(f"[Debug] 📞 Chamando API em: {API_URL}/api/v1/register")

    payload = {"email": email, "password": password}

    try:
        # Usamos a API_KEY_HEADERS (a chave de serviço) para registrar
        response = requests.post(
            f"{API_URL}/api/v1/register",
            headers=API_KEY_HEADERS,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        print(f"[Debug] 📞 API respondeu: {data}")
        return f"Usuário {data['email']} registrado com sucesso. Agora você pode fazer o login."

    except requests.exceptions.HTTPError as http_err:
        print(f"[Debug] ❌ Erro HTTP: {http_err.response.text}")
        return f"Erro ao registrar: {http_err.response.json().get('detail')}"
    except requests.exceptions.RequestException as e:
        print(f"[Debug] ❌ Erro de conexão: {e}")
        return "Não consegui conectar ao sistema. O servidor api.py está rodando?"


def login_user(email: EmailStr, password: str):
    """
    Loga o usuário no sistema e armazena o token de autenticação (crachá).
    """
    global USER_AUTH_TOKEN  # Vamos modificar a "memória"

    print(f"\n[Debug] 🤖 Gemini decidiu chamar: login_user(email='{email}')")
    print(f"[Debug] 📞 Chamando API em: {API_URL}/api/v1/login")

    payload = {"email": email, "password": password}

    try:
        # Usamos a API_KEY_HEADERS (a chave de serviço) para logar
        response = requests.post(
            f"{API_URL}/api/v1/login",
            headers=API_KEY_HEADERS,
            json=payload
        )
        response.raise_for_status()
        data = response.json()

        # --- PONTO-CHAVE ---
        # Guarda o token na nossa "memória"
        USER_AUTH_TOKEN = data['access_token']

        print(f"[Debug] 📞 API respondeu. Token armazenado!")
        return "Login realizado com sucesso! Agora você pode consultar seu saldo ou adicionar despesas."

    except requests.exceptions.HTTPError as http_err:
        print(f"[Debug] ❌ Erro HTTP: {http_err.response.text}")
        return f"Erro ao logar: {http_err.response.json().get('detail')}"
    except requests.exceptions.RequestException as e:
        print(f"[Debug] ❌ Erro de conexão: {e}")
        return "Não consegui conectar ao sistema. O servidor api.py está rodando?"


def get_saldo():
    """
    Busca o saldo atual DO USUÁRIO LOGADO.
    Falha se o usuário não estiver logado.
    """
    global USER_AUTH_TOKEN

    print(f"\n[Debug] 🤖 Gemini decidiu chamar: get_saldo()")

    # --- NOVO CHECK DE SEGURANÇA ---
    if USER_AUTH_TOKEN is None:
        print("[Debug] ❌ Usuário não está logado.")
        return "Você precisa fazer o login primeiro. Diga 'login' ou 'me logue'."

    # Prepara o "crachá" (Token JWT)
    auth_headers = {
        "Authorization": f"Bearer {USER_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    print(f"[Debug] 📞 Chamando API (com Token) em: {API_URL}/api/v1/saldo")
    try:
        # Faz a chamada GET usando o crachá
        response = requests.get(
            f"{API_URL}/api/v1/saldo",
            headers=auth_headers
        )
        response.raise_for_status()
        data = response.json()
        print(f"[Debug] 📞 API respondeu: {data}")
        return data  # Retorna o JSON do saldo

    except requests.exceptions.HTTPError as http_err:
        print(f"[Debug] ❌ Erro HTTP: {http_err.response.text}")
        if http_err.response.status_code == 401:
            USER_AUTH_TOKEN = None  # Limpa o token se ele expirou
            return "Seu login expirou. Por favor, faça o login novamente."
        return f"Erro da API: {http_err.response.text}"
    except requests.exceptions.RequestException as e:
        print(f"[Debug] ❌ Erro de conexão: {e}")
        return "Não consegui conectar ao sistema. O servidor api.py está rodando?"


def adicionar_despesa(valor: float, descricao: str, categoria: str):
    """
    Adiciona uma nova despesa para O USUÁRIO LOGADO.
    Falha se o usuário não estiver logado.
    """
    global USER_AUTH_TOKEN

    print(f"\n[Debug] 🤖 Gemini decidiu chamar: adicionar_despesa(valor={valor}, ...)")

    # --- NOVO CHECK DE SEGURANÇA ---
    if USER_AUTH_TOKEN is None:
        print("[Debug] ❌ Usuário não está logado.")
        return "Você precisa fazer o login primeiro para adicionar uma despesa."

    # Prepara o "crachá" (Token JWT)
    auth_headers = {
        "Authorization": f"Bearer {USER_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {"valor": valor, "descricao": descricao, "categoria": categoria}

    print(f"[Debug] 📞 Chamando API (com Token) em: {API_URL}/api/v1/despesas")
    try:
        # Faz a chamada POST usando o crachá
        response = requests.post(
            f"{API_URL}/api/v1/despesas",
            headers=auth_headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        print(f"[Debug] 📞 API respondeu: {data}")
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"[Debug] ❌ Erro HTTP: {http_err.response.text}")
        if http_err.response.status_code == 401:
            USER_AUTH_TOKEN = None  # Limpa o token se ele expirou
            return "Seu login expirou. Por favor, faça o login novamente."
        return f"Erro da API: {http_err.response.text}"
    except requests.exceptions.RequestException as e:
        print(f"[Debug] ❌ Erro de conexão: {e}")
        return "Não consegui conectar ao sistema. O servidor api.py está rodando?"


# --- 3. Configuração do Modelo Gemini ---

model = genai.GenerativeModel(
    model_name="models/gemini-pro-latest",
    # Passa TODAS as ferramentas que o Gemini pode usar
    tools=[register_user, login_user, get_saldo, adicionar_despesa]
)

# --- 4. O Chat (com "Automatic Function Calling") ---

chat = model.start_chat(enable_automatic_function_calling=True)

print("=" * 30)
print("🤖 Chatbot Financeiro (Gemini Pro) CONECTADO.")
print("    > Servidor da API: http://127.0.0.1:8000")
print("    > Gemini: OK (Modelo: gemini-pro-latest)")
print("=" * 30)
print("Você precisa se registrar e logar.")
print("Teste com: 'me registre com email meuemail@teste.com e senha 123456'")
print("Depois: 'meu login é meuemail@teste.com e senha 123456'")
print("Depois: 'qual meu saldo?'")
print("Digite 'sair' para terminar.")
print("=" * 30)

while True:
    prompt = input("Você: ")
    if prompt.lower() == 'sair':
        break

    try:
        response = chat.send_message(prompt)
        print(f"Gemini: {response.text}")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

print("Chat encerrado.")