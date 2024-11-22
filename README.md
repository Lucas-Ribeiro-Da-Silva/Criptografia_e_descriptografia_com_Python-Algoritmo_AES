# Sistema de Criptografia e Descriptografia de Dados Pessoais

Este repositório contém duas implementações: uma para **criptografar** e outra para **descriptografar** dados pessoais, como nomes, utilizando o algoritmo AES (Advanced Encryption Standard) com modo de operação CBC (Cipher Block Chaining). As implementações usam a biblioteca `cryptography` para realizar a criptografia e descriptografia de dados.

## Visão Geral

1. **Criptografia de Dados Pessoais**:
   - A primeira implementação realiza a criptografia de um nome usando o algoritmo AES-256 em modo CBC. A chave de criptografia e o vetor de inicialização (IV) são definidos de forma fixa para garantir a consistência entre os processos de criptografia e descriptografia.

2. **Descriptografia de Dados Pessoais**:
   - A segunda implementação descriptografa dados criptografados previamente, utilizando o mesmo algoritmo, chave e IV. Ele processa arquivos no formato Excel (`.xlsx`), descriptografando os nomes armazenados na coluna `NOME CRIPTOGRAFADO` e salvando o resultado em um novo arquivo com a coluna `NOME DESCRIPTOGRAFADO`.

## Requisitos

- **Python 3.x** ou superior
- Bibliotecas Python:
  - `pandas` (para manipulação de dados em formato de tabela)
  - `cryptography` (para criptografia e descriptografia)
  - `openpyxl` (para manipulação de arquivos Excel)
  
Você pode instalar essas dependências utilizando o seguinte comando:

```bash

pip install pandas cryptography openpyxl

```

# Uso

1. Defina uma chave de criptografia fixa (32 bytes para AES-256).
2. Carregue o nome ou dado que deseja criptografar.
3. Aplique a função de criptografia

**Atenção**: A chave e o vetor de inicialização (IV) devem ser os mesmos para garantir que os dados possam ser descriptografados corretamente.

### Estrutura do Projeto

criptografia.py           # Código responsável pela criptografia de dados <br>
descriptografia.py        # Código responsável pela descriptografia de dados <br>
DADOS_FICTICIOS.xlsx  # Exemplo de arquivo com dados ficticios para criptografar <br>
DADOS_FICTICIOS_CRIPTOGRAFADO.xlsx  # Arquivo gerado com dados criptografados <br>
DADOS_FICTICIOS_DESCRIPTOGRAFADO.xlsx  # Arquivo gerado com dados descriptografados

### Considerações de Segurança

Chave de Criptografia: A chave utilizada para criptografar os dados deve ser mantida em segurança, pois qualquer pessoa com acesso a ela pode descriptografar os dados. Evite utilizar chaves fixas em ambientes de produção;
Vetor de Inicialização (IV): O IV deve ser aleatório e único para cada operação de criptografia. No exemplo fornecido, o IV é fixo (iv = bytes([4] * 16)), o que não é recomendado para uso em ambientes de produção, mas no meu caso foi necessário para ter rastreabilidade dos dados criptografados.

