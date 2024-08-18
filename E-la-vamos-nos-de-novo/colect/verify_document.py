from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# Solicitar o nome do arquivo de assinatura
filename = input("Digite o nome do arquivo .sig para verificar (ex: documento_retornado_1_0.sig): ").strip()

# Carregando o payload salvo no arquivo
try:
    with open(filename, "rb") as f:
        payload_bytes = f.read()
except FileNotFoundError:
    print(f"Arquivo '{filename}' não encontrado.")
    exit(1)

# Carregando a chave pública
with open("keys/public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

# O conteúdo original do documento que foi assinado (ajuste conforme necessário)
with open("documento.txt", "rb") as f:
    original_document = f.read()

# Verificando a assinatura
try:
    public_key.verify(
        payload_bytes,
        original_document,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Assinatura verificada com sucesso!")

    # Salvando o conteúdo original do documento em "documento_retornado_descriptografado.txt"
    output_filename = filename.replace(".sig", "_descriptografado.txt")
    with open(output_filename, "wb") as f:
        f.write(original_document)
    print(f"Documento descriptografado salvo em '{output_filename}'")
except Exception as e:
    print(f"Falha na verificação da assinatura: {e}")
