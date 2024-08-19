def convert2bytes(hex_str):
    """
    Converte uma string hexadecimal para bytes.
    
    Parâmetros:
        hex_str (str): A string hexadecimal a ser convertida.
        
    Retorno:
        bytes: Os bytes resultantes da conversão.
    """
    # Remover o prefixo '0x' se estiver presente
    if hex_str.startswith("0x"):
        hex_str = hex_str[2:]
    
    # Converter a string hexadecimal para bytes
    return bytes.fromhex(hex_str)

# Solicitar o nome do arquivo de entrada
input_filename = input("Digite o nome do arquivo de entrada (ex: doc_rtn_0_0.hex): ").strip()

# Ler o conteúdo do arquivo de entrada
try:
    with open(input_filename, "r") as f:
        hex_content = f.read().strip()  # Lê o conteúdo e remove espaços em branco ao redor
except FileNotFoundError:
    print(f"Arquivo '{input_filename}' não encontrado.")
    exit(1)

# Converter o conteúdo de hexadecimal para bytes
try:
    byte_content = convert2bytes(hex_content)
except ValueError as e:
    print(f"Erro na conversão de hexadecimal para bytes: {e}")
    exit(1)

# Definir o nome do arquivo de saída com a mesma base do arquivo de entrada e extensão '.sig'
output_filename = f"{input_filename.rsplit('.', 1)[0]}.sig"

# Salvar o conteúdo convertido em bytes no arquivo de saída
with open(output_filename, "wb") as f:
    f.write(byte_content)

print(f"Conteúdo convertido salvo em '{output_filename}' com sucesso!")
