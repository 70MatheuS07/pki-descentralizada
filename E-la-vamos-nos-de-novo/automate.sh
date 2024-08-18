#!/bin/bash

# Executa o script de geração de chaves
echo "Gerando chaves..."
python3 keys/generate_keys.py

# Executa o script de assinatura de documento
echo "Assinando o documento..."
python3 sign/sign_document.py

echo "Transformando para hexadecimal..."
python3 hex/convert_hex.py

echo "Processo concluído!"

# Converte o conteúdo do arquivo para hexadecimal
hex_content=$(xxd -p documento_assinado_hex.txt | tr -d '\n')

# Executa o comando cartesi send generic com o input do arquivo
cartesi send generic --input "0x$hex_content" --input-encoding hex