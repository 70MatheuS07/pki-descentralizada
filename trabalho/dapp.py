from os import environ
import logging
import requests
import json
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import os

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

CERT_DIR = "./certificates"
REVOKED_CERT_DIR = "./certificates/revoked"
os.makedirs(CERT_DIR, exist_ok=True)
os.makedirs(REVOKED_CERT_DIR, exist_ok=True)

def save_certificate(cert_name, certificate):
    cert_path = os.path.join(CERT_DIR, cert_name)
    with open(cert_path, 'wb') as f:
        f.write(certificate)

def load_certificate(cert_name):
    cert_path = os.path.join(CERT_DIR, cert_name)
    with open(cert_path, 'rb') as f:
        return f.read()

def revoke_certificate(cert_name):
    cert_path = os.path.join(CERT_DIR, cert_name)
    revoked_cert_path = os.path.join(REVOKED_CERT_DIR, cert_name)
    os.rename(cert_path, revoked_cert_path)

def is_revoked(cert_name):
    revoked_cert_path = os.path.join(REVOKED_CERT_DIR, cert_name)
    return os.path.exists(revoked_cert_path)

def verify_certificate(public_key, certificate, signature):
    try:
        public_key.verify(
            signature,
            certificate,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return False

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    payload = json.loads(data["payload"])

    if "operation" not in payload:
        logger.error("Operation not specified in payload")
        return "reject"

    operation = payload["operation"]

    if operation == "register":
        cert_name = payload["cert_name"]
        certificate = payload["certificate"].encode()
        signature = bytes.fromhex(payload["signature"])
        public_key_pem = payload["public_key"].encode()

        public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())

        if verify_certificate(public_key, certificate, signature):
            save_certificate(cert_name, certificate)
            logger.info(f"Certificate {cert_name} registered successfully")
            return "accept"
        else:
            logger.error("Certificate verification failed")
            return "reject"

    elif operation == "revoke":
        cert_name = payload["cert_name"]
        signature = bytes.fromhex(payload["signature"])
        certificate = load_certificate(cert_name)

        if not certificate:
            logger.error(f"Certificate {cert_name} not found")
            return "reject"

        public_key = serialization.load_pem_public_key(certificate, backend=default_backend())

        if verify_certificate(public_key, certificate, signature):
            revoke_certificate(cert_name)
            logger.info(f"Certificate {cert_name} revoked successfully")
            return "accept"
        else:
            logger.error("Revocation verification failed")
            return "reject"

    else:
        logger.error(f"Unknown operation: {operation}")
        return "reject"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    payload = json.loads(data["payload"])
    cert_name = payload.get("cert_name")

    if is_revoked(cert_name):
        logger.info(f"Certificate {cert_name} is revoked")
        response = {"status": "revoked"}
    else:
        try:
            certificate = load_certificate(cert_name).decode('utf-8')
            logger.info(f"Certificate {cert_name} found")
            response = {"status": "valid", "certificate": certificate}
        except FileNotFoundError:
            logger.error(f"Certificate {cert_name} not found")
            response = {"status": "not found"}

    report = {"payload": json.dumps(response)}
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
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
