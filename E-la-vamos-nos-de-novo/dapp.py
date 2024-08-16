from os import environ
import logging
import requests

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def prepare_payload(data):
    # Converte a string original em hexadecimal e adiciona o prefixo 0x
    prefixed_hex_string = f"0x{data.encode('utf-8').hex()}"
    return prefixed_hex_string

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    
    # Exemplo de manipulação do payload (substitua conforme necessário)
    # Aqui assumo que `data["payload"]` contém a string que você deseja enviar
    if "payload" in data:
        original_string = data["payload"]
        hex_payload = prepare_payload(original_string)
        logger.info(f"Converted payload to hex: {hex_payload}")
        
        # Exemplo de envio do payload convertido para Cartesi Rollups
        response = requests.post(rollup_server + "/generic", json={"payload": hex_payload})
        logger.info(f"Sent payload to rollup, received status {response.status_code}")
        
    return "accept"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
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
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
