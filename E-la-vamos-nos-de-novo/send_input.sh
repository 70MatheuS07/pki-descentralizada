#!/bin/bash

# Converte o conteúdo do arquivo para hexadecimal
hex_content=$(xxd -p documento_assinado.sig | tr -d '\n')

# Executa o comando cartesi send generic com o input do arquivo
cartesi send generic --input "0x$hex_content" --input-encoding hex

# Envia 7 ENTERs
for i in {1..7}; do
    echo "" # Envia um ENTER
done
