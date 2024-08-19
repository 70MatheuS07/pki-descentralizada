from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# Solicitar o nome do arquivo de assinatura
filename = input("Digite o nome do arquivo .sig para verificar (ex: doc_rtn_0_0.sig): ").strip()

# Carregando a assinatura salva no arquivo
try:
    with open(filename, "rb") as f:
        signature = f.read()
except FileNotFoundError:
    print(f"Arquivo '{filename}' não encontrado.")
    exit(1)

# Carregando a chave pública
with open("keys/public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# Carregando o documento original que foi assinado
with open("documento.txt", "rb") as f:
    original_document = f.read()

# Verificando a assinatura
try:
    public_key.verify(
        signature,
        original_document,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Assinatura verificada com sucesso!")
except Exception as e:
    print(f"Falha na verificação da assinatura: {e}")
