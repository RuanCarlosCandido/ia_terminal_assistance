import requests
import sys
import json
import os
import time
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()
TOKEN = os.getenv("HUGGING_FACE_TOKEN")

# Verificar se o token está definido
if not TOKEN:
    print("Erro: O token da Hugging Face não foi encontrado. Verifique o arquivo .env.")
    sys.exit(1)

def carregar_modelos():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script Python
    models_path = os.path.join(script_dir, "models.json")    # Caminho completo para models.json
    
    with open(models_path, "r") as file:
        config = json.load(file)
    return config

# Função para listar modelos e escolher um
def escolher_modelo(config):
    print("Modelos disponíveis:")
    for model_number, model_info in config["models"].items():
        print(f"{model_number}: {model_info['name']}")

    # Solicitar que o usuário escolha um modelo pelo número
    modelo_escolhido = input("\nDigite o número do modelo que deseja usar (pressione Enter para usar o padrão): ")
    
    # Retorna o modelo escolhido ou o padrão, se nenhum for especificado
    return modelo_escolhido if modelo_escolhido in config["models"] else config["default"]

# Função principal para enviar a requisição
def gerar_resposta(prompt, modelo_url):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7
        }
    }
    
    while True:
        response = requests.post(modelo_url, headers=headers, json=data)
        
        # Verificar se o modelo está carregando
        if response.status_code == 503:
            error_info = response.json()
            if "estimated_time" in error_info:
                wait_time = error_info["estimated_time"]
                print(f"Modelo está carregando. Aguardando {wait_time} segundos antes de tentar novamente...")
                time.sleep(wait_time)
                continue
            else:
                print("Erro: Modelo está indisponível e não foi fornecido tempo estimado.")
                break
        elif response.status_code == 200:
            print(response.json()[0]["generated_text"])
            break
        else:
            print(f"Erro: {response.status_code}")
            print(response.json())
            break

# Carregar configuração de modelos
config = carregar_modelos()
modelos = config["models"]

# Verificar argumentos de linha de comando
if len(sys.argv) < 2:
    print("Uso: python huggingface_request.py <seu_prompt> ou python huggingface_request.py --list")
    sys.exit(1)

# Verificar se o usuário quer listar os modelos
if sys.argv[1] == "--list":
    modelo_escolhido = escolher_modelo(config)
    modelo_url = modelos[modelo_escolhido]["url"]
    
    # Solicitar o prompt do usuário
    prompt = input("\nDigite o prompt para o modelo selecionado: ")
else:
    # Usar o modelo padrão e capturar o prompt da linha de comando
    prompt = " ".join(sys.argv[1:])
    modelo_escolhido = config["default"]
    modelo_url = modelos[modelo_escolhido]["url"]

# Gerar a resposta usando o modelo selecionado
print(f"\nUsando o modelo '{modelos[modelo_escolhido]['name']}' para o prompt:\n")
gerar_resposta(prompt, modelo_url)

