# Ler o arquivo assinado
with open("documento_assinado.sig", "rb") as f:
    signed_document = f.read()

# Converter o conteúdo para hexadecimal
hex_signed_document = signed_document.hex()

# Salvando o conteúdo hexadecimal em um novo arquivo
with open("documento_assinado_hex.txt", "w") as f:
    f.write(hex_signed_document)

print(f"Documento assinado convertido para hexadecimal com sucesso! Hex salvo em 'documento_assinado_hex.txt'")
