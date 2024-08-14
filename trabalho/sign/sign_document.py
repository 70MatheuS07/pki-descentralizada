# trabalho/sign/sign_document.py

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# Carregando a chave privada
with open("keys/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Lendo o documento
with open("sign/documento.txt", "rb") as f:
    document = f.read()

# Assinando o documento
signature = private_key.sign(
    document,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Salvando a assinatura
with open("sign/signature.sig", "wb") as f:
    f.write(signature)
