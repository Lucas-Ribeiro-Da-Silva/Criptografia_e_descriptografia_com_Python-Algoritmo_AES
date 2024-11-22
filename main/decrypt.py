import pandas as pd
import ast
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Define uma chave fixa para o algoritmo AES (deve ter 32 bytes para AES-256)
fixed_key = b'!TroqueSuaChaveFixaAqui_32bytes!'

# Função que cria um cifrador AES com um vetor de inicialização (IV) fixo
def create_cipher(key, iv):
    """Cria e retorna um objeto de cifra AES com o vetor de inicialização (IV) fornecido."""
    return Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

# Função para descriptografar um texto
def decrypt_text(key, ciphertext):
    """Descriptografa um texto criptografado com a chave fornecida e retorna o texto original."""
    iv = bytes([4] * 16)  # O vetor de inicialização (IV) deve ser o mesmo utilizado na criptografia
    cipher = create_cipher(key, iv)  # Cria a cifra AES com o IV
    decryptor = cipher.decryptor()  # Cria um objeto para realizar a descriptografia
    
    # Descriptografa o texto criptografado
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove o preenchimento PKCS7
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()  # Retorna o texto original (decodificado)

# Função para descriptografar um nome
def decrypt_name(ciphertext):
    """Descriptografa um nome e retorna o valor descriptografado."""
    if pd.isna(ciphertext):  # Verifica se o valor é NaN
        return None  # Retorna None se o valor for NaN

    try:
        # Converte a string de bytes que está no formato de representação Python para o formato de bytes
        if isinstance(ciphertext, str):
            byte_string = ast.literal_eval(ciphertext)  # Avalia a string para obter os bytes
        else:
            byte_string = ciphertext  # Caso o valor já seja bytes
        
        return decrypt_text(fixed_key, byte_string)  # Retorna o nome descriptografado
    except Exception as e:
        print(f'Erro ao descriptografar: {e}')  # Exibe erro caso ocorra
        return None  # Retorna None se a conversão falhar

# Função para processar a descriptografia dos nomes de um arquivo Excel
def decrypt_excel_column(file_path):
    """Carrega um arquivo Excel, descriptografa a coluna 'NOME CRIPTOGRAFADO' e salva o resultado em um novo arquivo."""
    # Carrega o arquivo Excel em um DataFrame
    df = pd.read_excel(file_path)
    
    # Aplica a função de descriptografia para a coluna 'NOME CRIPTOGRAFADO' e cria uma nova coluna
    df['NOME DESCRIPTOGRAFADO'] = df['NOME CRIPTOGRAFADO'].apply(decrypt_name)

    # Exclui a coluna 'NOME CRIPTOGRAFADO' após a descriptografia
    colunas_para_excluir = ['NOME CRIPTOGRAFADO']
    df.drop(columns=colunas_para_excluir, inplace=True, errors='ignore')

    # Obtém a última coluna e as colunas restantes
    last_columns = df.iloc[:, -1:]
    remaining_columns = df.iloc[:, :-1]

    # Combina a última coluna com as colunas restantes
    df = pd.concat([last_columns, remaining_columns], axis=1)

    # Salva o DataFrame resultante em um novo arquivo Excel
    df.to_excel('./DADOS_FICTICIOS_DESCRIPTOGRAFADO.xlsx', index=False)

# Chama a função para descriptografar o arquivo
decrypt_excel_column('./DADOS_FICTICIOS_CRIPTOGRAFADO.xlsx')
