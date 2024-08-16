# Abrir o arquivo em modo binário
with open('documento_assinado.sig', 'rb') as file:
    # Ler o conteúdo do arquivo
    file_content = file.read()

# Converter o conteúdo em hexadecimal
hex_content = file_content.hex()

# Exibir o resultado
print(hex_content)
