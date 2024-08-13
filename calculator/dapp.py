from os import environ
import logging
import requests
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os

# Configurações de logging
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

# URL do servidor de Rollups (Cartesi)
rollup_server = environ.get("ROLLUP_HTTP_SERVER_URL", "http://127.0.0.1:5004")
logger.info(f"HTTP rollup_server url is {rollup_server}")

# Geração de chaves e assinatura
def gerar_chaves_e_assinar(documento_path):
    # Verificar se o arquivo existe
    if not os.path.exists(documento_path):
        logger.error(f"Erro: O documento '{documento_path}' não existe.")
        return None

    # Ler o documento a ser assinado
    with open(documento_path, "rb") as doc_file:
        documento = doc_file.read()

    # Gerar a chave privada
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Salvar a chave privada em um arquivo .pem
    with open("chave_privada.pem", "wb") as private_file:
        private_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Extrair a chave pública
    public_key = private_key.public_key()

    # Salvar a chave pública em um arquivo .pem
    with open("chave_publica.pem", "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    # Assinar o documento
    assinatura = private_key.sign(
        documento,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # Salvar a assinatura em um arquivo
    with open("assinatura.bin", "wb") as assinatura_file:
        assinatura_file.write(assinatura)

    logger.info("Chaves e assinatura geradas com sucesso!")
    return assinatura, documento

# Função para manipular requests do tipo "advance"
def handle_advance(data):
    logger.info(f"Received advance request data: {data}")
    
    try:
        # Obtenha o payload do input recebido
        payload = data.get("payload")
        if not payload:
            logger.error("Payload não encontrado.")
            return "reject"
        
        # Decodifique o payload de hex para string
        decoded_payload = bytes.fromhex(payload[2:]).decode('utf-8')

        # Verificar se o payload é um comando especial
        if decoded_payload == 'SIGN_DOCUMENT':
            logger.info("Comando 'SIGN_DOCUMENT' recebido. Usando documento padrão para assinatura.")
            documento_path = "meu_documento.txt"  # Nome padrão do documento
            result = gerar_chaves_e_assinar(documento_path)
            if result:
                assinatura, documento = result
                logger.info(f"Assinatura gerada: {assinatura.hex()}")
                return "accept"
            else:
                return "reject"
        
        # Se o payload for um caminho de arquivo, tentar assinar o documento
        elif os.path.exists(decoded_payload):
            logger.info(f"Processando o documento: {decoded_payload}")
            result = gerar_chaves_e_assinar(decoded_payload)
            if result:
                assinatura, documento = result
                logger.info(f"Assinatura gerada: {assinatura.hex()}")
                return "accept"
            else:
                return "reject"

        logger.error("Comando inválido ou arquivo não encontrado.")
        return "reject"

    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {str(e)}")
        return "reject"

# Função para manipular requests do tipo "inspect"
def handle_inspect(data):
    logger.info(f"Received inspect request data: {data}")
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
