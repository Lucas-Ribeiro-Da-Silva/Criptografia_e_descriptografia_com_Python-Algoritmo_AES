import pandas as pd
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# Define uma chave fixa para o algoritmo AES (Recomenda-se usar um método seguro de gerenciamento de chaves)
fixed_key = b'!TroqueSuaChaveFixaAqui_32bytes!'  # Deve ter 32 bytes para AES-256

# Função que cria um cifrador AES com um vetor de inicialização (IV) fixo
def create_cipher(key, iv):
    """
    Cria um objeto de cifrador AES com um IV fixo.
    
    :param key: Chave de criptografia de 32 bytes (AES-256)
    :param iv: Vetor de Inicialização (IV) de 16 bytes
    :return: Objeto Cipher configurado para o algoritmo AES com CBC
    """
    return Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

# Função para criptografar um texto
def encrypt_text(key, plaintext):
    """
    Criptografa o texto fornecido utilizando AES com modo CBC e preenchimento PKCS7.
    
    :param key: Chave de criptografia de 32 bytes (AES-256)
    :param plaintext: Texto a ser criptografado
    :return: Texto criptografado em bytes
    """
    iv = bytes([4] * 16)  # Define um vetor de inicialização (IV) fixo de 16 bytes
    cipher = create_cipher(key, iv)  # Cria o cifrador
    encryptor = cipher.encryptor()  # Cria o objeto para criptografar
    
    # Aplica o preenchimento PKCS7 para garantir que o tamanho do texto seja múltiplo do bloco
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_text = padder.update(plaintext.encode()) + padder.finalize()
    
    return encryptor.update(padded_text) + encryptor.finalize()

def encrypt_name(name):
    """
    Criptografa o nome, substituindo valores inválidos por '-'.
    
    :param name: Nome a ser criptografado
    :return: Nome criptografado ou '-' caso o nome seja inválido
    """
    if pd.isna(name) or name == '-' or name == '':
        return '-'
    return encrypt_text(fixed_key, str(name))

# Caminho dos arquivos de entrada e saída
arquivo_entrada = './DADOS_FICTICIOS.xlsx'
arquivo_saida = './DADOS_FICTICIOS_CRIPTOGRAFADO.xlsx'

try:
    # Lê o arquivo Excel de entrada
    df = pd.read_excel(arquivo_entrada, engine='openpyxl')
    
    # Substitui valores NaN por "-"
    df.fillna('-', inplace=True)

    # Criptografa a coluna 'NOME'
    df['NOME CRIPTOGRAFADO'] = df['NOME'].apply(encrypt_name)

    # Exclui a coluna 'NOME' após criptografar
    df.drop(columns=['NOME'], inplace=True, errors='ignore')

    # Formata a coluna de data para o formato 'dd/mm/yyyy'
    df['DATA DE NASCIMENTO'] = pd.to_datetime(df['DATA DE NASCIMENTO'], errors='coerce').dt.strftime('%d/%m/%Y')

    # Move a coluna 'NOME CRIPTOGRAFADO' para a primeira posição
    df = pd.concat([df[['NOME CRIPTOGRAFADO']], df.drop(columns=['NOME CRIPTOGRAFADO'])], axis=1)

    # Salva o DataFrame criptografado em um novo arquivo Excel
    with pd.ExcelWriter(arquivo_saida, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='CRIPTOGRAFADO')
        
        # Formatação do arquivo Excel
        workbook = writer.book
        worksheet = writer.sheets['CRIPTOGRAFADO']
        cell_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        worksheet.set_column('A:ZZ', None, cell_format)

        header_format = workbook.add_format({
            'bg_color': '#A6C9EC',  # Azul de fundo
            'color': 'black',  # Texto preto
            'bold': True,  # Negrito
            'align': 'center',  # Alinhamento horizontal centralizado
            'valign': 'vcenter'  # Alinhamento vertical centralizado
        })

        # Aplica formatação no cabeçalho
        for col_num, col in enumerate(df.columns):
            worksheet.write(0, col_num, col, header_format)

    print(f"Processamento concluído! O resultado foi salvo em '{arquivo_saida}'.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")
