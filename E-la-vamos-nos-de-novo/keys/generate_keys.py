# trabalho/keys/generate_keys.py

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Gerando chave privada
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Serializando e salvando a chave privada
with open("keys/private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Gerando chave pública
public_key = private_key.public_key()

# Serializando e salvando a chave pública
with open("keys/public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("Chaves privada e pública geradas com sucesso!")