from flask import Flask, request, jsonify
from web3 import Web3
import json

app = Flask(__name__)

# Conectar ao Ganache
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Verificar se a conexão foi bem-sucedida
if not web3.is_connected():
    raise Exception("Erro ao conectar ao Ganache")

# Carregar o ABI do contrato
with open('build/contracts/PKI.json') as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']

# Endereço do contrato implantado
contract_address = '0x36C02dA8a0983159322a80FFE9F24b1acfF8B570'
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/register_certificate', methods=['POST'])
def register_certificate():
    data = request.json
    certificate_hash = data['certificate_hash']
    
    tx_hash = contract.functions.registerCertificate(certificate_hash).transact({'from': web3.eth.accounts[0]})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return jsonify({'transaction_receipt': receipt})

@app.route('/revoke_certificate', methods=['POST'])
def revoke_certificate():
    data = request.json
    certificate_hash = data['certificate_hash']
    
    tx_hash = contract.functions.revokeCertificate(certificate_hash).transact({'from': web3.eth.accounts[0]})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return jsonify({'transaction_receipt': receipt})

@app.route('/verify_certificate', methods=['POST'])
def verify_certificate():
    data = request.json
    certificate_hash = data['certificate_hash']
    
    is_valid = contract.functions.verifyCertificate(certificate_hash).call()
    
    return jsonify({'is_valid': is_valid})

if __name__ == '__main__':
    app.run(debug=True)
