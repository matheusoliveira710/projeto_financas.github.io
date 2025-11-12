import google.generativeai as genai
import os

print("--- Iniciando Verificador de Modelos Gemini (Modo Direto) ---")

try:
    # Vamos colocar a chave direto aqui, para não depender do terminal
    key = "AIzaSyAS3FKdGlhcU4Rtaw1hYNn4kYYSDUyQYkg" 
    
    print("Chave definida diretamente no script.")
    genai.configure(api_key=key)

    print("\nBuscando modelos disponíveis para esta chave...")
    print("="*40)
    
    found_model = False
    # Lista todos os modelos que a Google disponibiliza para sua chave
    for model in genai.list_models():
        # Vamos focar apenas nos modelos que sabem "conversar"
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ Modelo compatível encontrado: {model.name}")
            found_model = True

    print("="*40)
    
    if not found_model:
        print("❌ Nenhum modelo compatível com 'generateContent' foi encontrado.")
        print("Isso é estranho. Verifique se sua chave API está correta")
        print("e se sua conta no Google AI Studio está ativa.")
    else:
        print("🚀 Sucesso!")
        print("Por favor, copie um dos nomes de modelo da lista acima")
        print("(Ex: 'models/gemini-pro') e cole no 'model_name=' do seu chatbot.py.")

except Exception as e:
    print(f"\nOcorreu um erro inesperado ao tentar listar os modelos: {e}")

print("--- Verificação concluída ---")