from os import environ
import logging
import requests
import os

# Configurações de log
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

# URL do servidor Rollup
rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

# Diretório onde os arquivos enviados serão salvos
UPLOAD_DIRECTORY = "/path/to/upload/directory"

# Certifique-se de que o diretório de upload exista
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    return "accept"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    return "accept"

def handle_upload(data):
    # Supondo que 'data' contenha o nome do arquivo e o conteúdo do arquivo em formato base64
    file_name = data.get("file_name")
    file_content = data.get("file_content")

    if not file_name or not file_content:
        logger.error("Missing file_name or file_content in upload data")
        return "reject"

    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)

    try:
        with open(file_path, "wb") as file:
            file.write(file_content.encode('utf-8'))
        logger.info(f"File {file_name} uploaded successfully")
        return "accept"
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        return "reject"

# Dicionário de manipuladores
handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
    "upload_document": handle_upload,
}

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
        handler = handlers.get(rollup_request["request_type"])

        if handler:
            finish["status"] = handler(data)
        else:
            logger.error(f"No handler found for request type {rollup_request['request_type']}")
            finish["status"] = "reject"
