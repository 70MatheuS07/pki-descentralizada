import json
import base64

# Caminho para o arquivo criptografado
file_path = "signature.sig"

# Ler o conteúdo binário do arquivo
with open(file_path, "rb") as file:
    file_content = file.read()

# Codificar o conteúdo do arquivo em base64
encoded_content = base64.b64encode(file_content).decode('utf-8')

# Criar o payload JSON com o conteúdo codificado
payload = {
    "document": encoded_content
}

# Escrever o payload no arquivo payload.json
with open("payload.json", "w") as json_file:
    json.dump(payload, json_file)

print("Arquivo payload.json gerado com sucesso.")
