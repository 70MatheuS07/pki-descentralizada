import os
from os import environ
import logging
import requests
import json
import base64

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    
    payload = json.loads(data["payload"])
    encoded_document = payload.get("document", "")
    
    if encoded_document:
        # Decodificar o conteúdo base64 de volta para binário
        document_content = base64.b64decode(encoded_document)
        
        # Processar o conteúdo do documento (neste exemplo, estamos apenas logando)
        logger.info(f"Decoded document content: {document_content}")
        
        # Enviar uma notificação de que o documento foi processado
        response = requests.post(rollup_server + "/notice", json={"payload": "Documento processado com sucesso"})
        logger.info(f"Received notice status {response.status_code} body {response.content}")
    else:
        logger.warning("No document found in payload")
    
    return "accept"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    # Lógica para inspeção
    report = {"payload": data["payload"]}
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")
    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
