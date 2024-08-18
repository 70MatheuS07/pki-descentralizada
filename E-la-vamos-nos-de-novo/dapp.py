import json
from os import environ
import logging
import requests
import os

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

# Obter a URL do servidor Rollup
rollup_server = os.getenv("ROLLUP_HTTP_SERVER_URL")
print(f"HTTP rollup_server url is {rollup_server}")

global users
global saveTotal

# Função para converter hexadecimal para string
def hex2str(hex_str):
    # Remove o prefixo '0x' se estiver presente
    if hex_str.startswith("0x"):
        hex_str = hex_str[2:]
    
    # Converte o hexadecimal para bytes e depois para string, ignorando erros
    return bytes.fromhex(hex_str).decode('utf-8')


# Função para converter string para hexadecimal
def str2hex(payload):
    # Converte a string para bytes e depois para hexadecimal
    return "0x" + payload.encode('utf-8').hex()

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    
    metadata = data["metadata"]
    sender = metadata["msg_sender"]
    payload = data["payload"]

    sentence = hex2str(payload)

    # Inicialize saveTotal antes de usá-lo
    global saveTotal
    if 'saveTotal' not in globals():
        saveTotal = 0

    # Inicialize saveTotal antes de usá-lo
    global users
    if 'users' not in globals():
        users = []

    users.append(sender)
    saveTotal += 1

    # Corpo da requisição em JSON
    payload = json.dumps({ "payload": str2hex(sentence) })

    # Fazendo a requisição POST
    notice_req = requests.post(
        url=rollup_server + "/notice",
        headers={"Content-Type": "application/json"},
        data=payload
    )

    return "accept"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")

    payload = data["payload"]
    route = hex2str(payload)
    
    responseObject = {}
    if route == "list":
        responseObject = json.dumps(users, separators=(',', ':'))
    elif route == "total":
        responseObject = json.dumps(saveTotal, separators=(',', ':'))
    else:
        responseObject = "route not implemented"

    # Corpo da requisição em JSON
    payload = json.dumps({ "payload": str2hex(responseObject) })

    # Fazendo a requisição POST
    report_req = requests.post(
        url=rollup_server + "/report",
        headers={"Content-Type": "application/json"},
        data=payload
    )

    # Verificando a resposta
    print("STATUS_CODE:" + report_req.status_code)
    print("JSON:" + report_req.json())

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
