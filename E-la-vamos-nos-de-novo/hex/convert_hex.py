# Ler o arquivo assinado
with open("doc_sign.sig", "rb") as f:
    signed_document = f.read()

# Converter o conteúdo para hexadecimal
hex_signed_document = signed_document.hex()

# Salvando o conteúdo hexadecimal em um novo arquivo
with open("doc_sign.hex", "w") as f:
    f.write(hex_signed_document)

print(f"Documento assinado convertido para hexadecimal com sucesso! Hex salvo em 'doc_sign.hex'")
