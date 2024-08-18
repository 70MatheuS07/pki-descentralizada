import requests
import json

# URL do servidor GraphQL
url = "http://localhost:8080/graphql"

# A query GraphQL para obter todos os documentos
query = """
query notices {
  notices {
    edges {
      node {
        index
        input {
          index
        }
        payload
      }
    }
  }
}
"""

# Cabeçalhos da requisição
headers = {"Content-Type": "application/json"}

# Função para converter hexadecimal para bytes
def hex_to_bytes(hex_str):
    if hex_str.startswith("0x"):
        hex_str = hex_str[2:]
    return bytes.fromhex(hex_str)

# Solicitar o tipo de índice ao usuário
index_type = input("Deseja buscar pelo index do node ou do input? (Digite 'node' ou 'input'): ").strip().lower()
index_requested = input("Digite o número do índice que deseja coletar: ").strip()

# Fazendo a requisição POST para o GraphQL endpoint
response = requests.post(url, json={"query": query}, headers=headers)

# Verifique se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    # Extraindo os documentos (notices) da resposta
    notices = data.get("data", {}).get("notices", {}).get("edges", [])
    
    # Procurando o documento com o índice solicitado
    for notice in notices:
        node_index = notice["node"]["index"]
        input_index = notice["node"]["input"]["index"]
        
        if (index_type == "node" and str(node_index) == index_requested) or \
           (index_type == "input" and str(input_index) == index_requested):
            payload_hex = notice["node"]["payload"]
            print(f"Processando documento com node index {node_index} e input index {input_index} com payload: {payload_hex}")
            
            # Converte o payload para bytes
            payload_bytes = hex_to_bytes(payload_hex)
            
            # Salva o payload em "documento_retornado_{node_index}_{input_index}.sig"
            filename = f"documento_retornado_{node_index}_{input_index}.sig"
            with open(filename, "wb") as f:
                f.write(payload_bytes)
            print(f"Payload salvo em '{filename}'")
            break
    else:
        print(f"Documento com índice {index_requested} não encontrado.")
else:
    print(f"Falha na requisição GraphQL. Status code: {response.status_code}")
