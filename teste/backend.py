from flask import Flask, request, jsonify
import base64
import json

app = Flask(__name__)

@app.route('/input', methods=['POST'])
def process_input():
    # Recebe o JSON enviado no corpo da requisição
    payload = request.get_json()

    # Verifica se o campo 'document' existe no payload
    if 'document' in payload:
        # Decodifica o conteúdo do documento de base64 para binário
        document_content = base64.b64decode(payload['document'])

        # Para fins de exemplo, vamos salvar o documento decodificado em um arquivo
        with open('decoded_document.sig', 'wb') as f:
            f.write(document_content)

        # Retorna uma resposta de sucesso
        return jsonify({"status": "success", "message": "Document received and processed."}), 200
    else:
        return jsonify({"status": "error", "message": "No document found in payload."}), 400

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
