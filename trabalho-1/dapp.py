from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# Gerar a chave privada
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Salvar a chave privada em um arquivo .pem
with open("chave_privada.pem", "wb") as private_file:
    private_file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Extrair a chave pública
public_key = private_key.public_key()

# Salvar a chave pública em um arquivo .pem
with open("chave_publica.pem", "wb") as public_file:
    public_file.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

# Documento a ser assinado (codificado em UTF-8)
documento = "Este é o conteúdo do documento que será assinado.".encode('utf-8')

# Assinar o documento
assinatura = private_key.sign(
    documento,
    padding.PKCS1v15(),
    hashes.SHA256()
)

# Verificar a assinatura
try:
    public_key.verify(
        assinatura,
        documento,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("Assinatura verificada com sucesso!")
except:
    print("Falha na verificação da assinatura!")
