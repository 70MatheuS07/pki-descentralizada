from flask import Flask, request, jsonify
from os import environ
import logging
import requests
import contract_manager as cm

app = Flask(__name__)

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ.get("ROLLUP_HTTP_SERVER_URL")
logger.info(f"HTTP rollup_server url is {rollup_server}")

finish = {"status": "accept"}

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    # Adapte esta lógica conforme necessário
    # Por exemplo, se você quiser registrar um certificado
    certificate_hash = data.get("certificate_hash")
    if certificate_hash:
        receipt = cm.register_certificate(certificate_hash)
        return "accept" if receipt else "reject"
    return "reject"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    # Adapte esta lógica conforme necessário
    # Por exemplo, se você quiser verificar um certificado
    certificate_hash = data.get("certificate_hash")
    if certificate_hash:
        is_valid = cm.verify_certificate(certificate_hash)
        return "accept" if is_valid else "reject"
    return "reject"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

@app.route('/process_rollup_requests', methods=['POST'])
def process_rollup_requests():
    while True:
        logger.info("Sending finish")
        response = requests.post(rollup_server + "/finish", json=finish)
        logger.info(f"Received finish status {response.status_code}")
        if response.status_code == 202:
            logger.info("No pending rollup request, trying again")
        else:
            rollup_request = response.json()
            data = rollup_request.get("data", {})
            request_type = rollup_request.get("request_type")
            handler = handlers.get(request_type)
            if handler:
                finish["status"] = handler(data)
            else:
                finish["status"] = "reject"
        # Adicione um delay se necessário para evitar excesso de requisições
        time.sleep(10)  # Ajuste o tempo conforme necessário

    return jsonify({'status': finish["status"]})

if __name__ == '__main__':
    app.run(debug=True)
