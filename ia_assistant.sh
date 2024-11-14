#!/bin/bash

# Diretório onde o script Python está localizado, relativo ao script atual
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PYTHON="$SCRIPT_DIR/huggingface_request.py"

# Exibir uma saudação inicial
echo "Olá! Como posso ajudar? (Digite 'sair' para encerrar a sessão)"

# Iniciar um loop interativo
while true; do
    # Ler a entrada do usuário
    read -p "> " prompt

    # Verificar se o usuário digitou 'sair' para encerrar
    if [[ "$prompt" == "sair" ]]; then
        echo "Até logo!"
        break
    fi

    # Enviar o prompt para o script Python e exibir a resposta
    python3 "$SCRIPT_PYTHON" "$prompt"
done

