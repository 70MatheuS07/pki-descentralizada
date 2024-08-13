#!/bin/bash

DOCUMENTO="documento.txt"
HEX_PAYLOAD=$(echo -n $DOCUMENTO | xxd -p | tr -d '\n')

# Enviar o input usando curl
curl -X POST http://localhost:5004/finish -H "Content-Type: application/json" \
-d "{\"payload\": \"0x$HEX_PAYLOAD\"}"
