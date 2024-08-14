#!/bin/bash

# Caminho para o diretório do projeto
PROJECT_DIR=$(dirname "$0")

# Executando o script de geração de chaves
echo "Gerando chaves..."
python3 "$PROJECT_DIR/keys/generate_keys.py"

# Executando o script de assinatura de documento
echo "Assinando o documento..."
python3 "$PROJECT_DIR/sign/sign_document.py"

# Mensagem final
echo "Todas as etapas foram concluídas com sucesso!"
