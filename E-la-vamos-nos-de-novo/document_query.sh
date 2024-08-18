#!/bin/bash

echo "Coletando o documento com index específico..."
python3 colect/colect_document.py

echo "Verificando o documento com index específico..."
python3 colect/verify_document.py