from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# Solicitar o nome do documento ao usuário
document_name = input("Informe o nome do documento (com extensão): ")

# Carregando a chave privada
with open("keys/private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Lendo o documento
with open(document_name, "rb") as f:
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

# Salvando a assinatura com o nome do documento original + ".sig"
signed_document_name = f"documento_assinado.sig"
with open(signed_document_name, "wb") as f:
    f.write(signature)

print(f"Documento '{document_name}' assinado com sucesso! Assinatura salva em '{signed_document_name}'")
