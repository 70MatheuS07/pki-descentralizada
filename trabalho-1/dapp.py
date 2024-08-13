from os import environ
import logging
import json
import requests
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# Configurações de logging
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

# URL do servidor de Rollups (Cartesi)
rollup_server = environ.get("ROLLUP_HTTP_SERVER_URL", "http://127.0.0.1:5004")
logger.info(f"HTTP rollup_server url is {rollup_server}")

# Função para verificar a assinatura
def verificar_assinatura(public_key_pem, assinatura, documento):
    try:
        # Carregar a chave pública
        public_key = serialization.load_pem_public_key(public_key_pem)

        # Verificar a assinatura
        public_key.verify(
            assinatura,
            documento,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        logger.info("Assinatura verificada com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Falha na verificação da assinatura: {str(e)}")
        return False

# Função para manipular requests do tipo "advance"
def handle_advance(data):
    logger.info(f"Received advance request data: {data}")
    
    try:
        # Supondo que o payload contém a assinatura e o documento (codificados em hex)
        payload = data.get("payload")
        if not payload:
            logger.error("Payload não encontrado.")
            return "reject"
        
        # Decodificar o payload do formato hexadecimal
        payload_data = bytes.fromhex(payload[2:])  # Remover o prefixo "0x"
        
        # Separar a assinatura e o documento (essa estrutura depende de como você embala esses dados)
        assinatura = payload_data[:256]  # Supondo que a assinatura tenha 256 bytes
        documento = payload_data[256:]  # O restante é o documento

        # Carregar a chave pública a partir do arquivo PEM
        with open("chave_publica.pem", "rb") as key_file:
            public_key_pem = key_file.read()

        # Verificar a assinatura
        if verificar_assinatura(public_key_pem, assinatura, documento):
            # Processar o documento se a assinatura for válida
            logger.info("Documento processado com sucesso.")
            return "accept"
        else:
            return "reject"
    
    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {str(e)}")
        return "reject"

# Função para manipular requests do tipo "inspect"
def handle_inspect(data):
    logger.info(f"Received inspect request data: {data}")
    logger.info("Adding report")
    report = {"payload": data["payload"]}
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")
    return "accept"

# Dicionário de handlers
handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

# Loop principal do dApp
finish = {"status": "accept"}
while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]

        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(data)
