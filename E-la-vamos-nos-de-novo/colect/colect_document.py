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

# Solicitar os índices ao usuário
node_index_requested = input("Digite o número do index do node que deseja coletar: ").strip()
input_index_requested = input("Digite o número do index do input que deseja coletar: ").strip()

# Fazendo a requisição POST para o GraphQL endpoint
response = requests.post(url, json={"query": query}, headers=headers)

# Verifique se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    # Extraindo os documentos (notices) da resposta
    notices = data.get("data", {}).get("notices", {}).get("edges", [])
    
    # Procurando o documento com os índices solicitados
    for notice in notices:
        node_index = notice["node"]["index"]
        input_index = notice["node"]["input"]["index"]
        
        if str(node_index) == node_index_requested and str(input_index) == input_index_requested:
            payload_hex = notice["node"]["payload"]
            print(f"Processando documento com node index {node_index} e input index {input_index} com payload: {payload_hex}")
            
            # Converte o payload para bytes
            payload_bytes = hex_to_bytes(payload_hex)
            
            # Salva o payload em "doc_rtn_{node_index}_{input_index}.sig"
            filename = f"doc_rtn_{node_index}_{input_index}.hex"
            with open(filename, "wb") as f:
                f.write(payload_bytes)
            print(f"Payload salvo em '{filename}'")
            break
    else:
        print(f"Documento com node index {node_index_requested} e input index {input_index_requested} não encontrado.")
else:
    print(f"Falha na requisição GraphQL. Status code: {response.status_code}")
