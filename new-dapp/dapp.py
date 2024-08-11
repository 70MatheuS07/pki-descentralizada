from flask import Flask, request, jsonify
import web3
from web3 import Web3

app = Flask(__name__)

# Inicialização do web3 e do contrato (exemplo simplificado)
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
contract_address = 'SEU_ENDEREÇO_DO_CONTRATO'
contract_abi = 'SEU_ABI_DO_CONTRATO'
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/register_certificate', methods=['POST'])
def register_certificate():
    data = request.json
    certificate_hash = data['certificate_hash']

    # Convertendo o hash do certificado para bytes32
    certificate_hash_bytes = Web3.toBytes(hexstr=certificate_hash)

    # Transacionar com o contrato
    tx_hash = contract.functions.registerCertificate(certificate_hash_bytes).transact({'from': web3.eth.accounts[0]})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return jsonify({'transaction_receipt': receipt})

if __name__ == '__main__':
    app.run(debug=True)
