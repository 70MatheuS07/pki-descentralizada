#!/bin/bash

# Diretório onde o script está localizado
TARGET_DIR="$(dirname "$(realpath "$0")")"

# Arquivos de nome fixo para remover
FIXED_FILES=("doc_sign.hex" "doc_sign.sig")

# Remove arquivos de nome fixo
for FILE in "${FIXED_FILES[@]}"; do
    if [ -e "$TARGET_DIR/$FILE" ]; then
        echo "Removendo $TARGET_DIR/$FILE"
        rm "$TARGET_DIR/$FILE"
    else
        echo "Arquivo $TARGET_DIR/$FILE não encontrado"
    fi
done

# Remove arquivos que seguem o padrão doc_rtn_x_y
echo "Removendo arquivos no padrão doc_rtn_x_y"
for FILE in "$TARGET_DIR"/doc_rtn_*_*; do
    if [ -e "$FILE" ]; then
        echo "Removendo $FILE"
        rm "$FILE"
    else
        echo "Nenhum arquivo correspondente encontrado para o padrão doc_rtn_x_y"
    fi
done

echo "Limpeza concluída."
