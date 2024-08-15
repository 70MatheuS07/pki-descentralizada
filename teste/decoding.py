from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def verify_signature(public_key_path, signature_path, message_path):
    # Carregar a chave pública
    with open(public_key_path, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
    
    # Carregar a assinatura
    with open(signature_path, 'rb') as sig_file:
        signature = sig_file.read()
    
    # Carregar a mensagem original
    with open(message_path, 'rb') as msg_file:
        message = msg_file.read()
    
    try:
        # Verificar a assinatura
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("A assinatura é válida.")
    except Exception as e:
        print("A assinatura não é válida.", e)

# Caminhos para os arquivos
public_key_path = 'public_key.pem'
signature_path = 'signature.sig'
message_path = 'documento.txt'  # O arquivo que contém a mensagem original que foi assinada

# Verificar a assinatura
verify_signature(public_key_path, signature_path, message_path)
