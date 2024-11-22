# Criptografia e descriptografia com Python - Algoritmo AES

O código apresentado utiliza o algoritmo AES (Advanced Encryption Standard) no modo CBC (Cipher Block Chaining) para realizar a criptografia. Algumas características importantes do uso deste algoritmo no código:

- Chave de Criptografia:
A chave utilizada para o AES é fixa e definida pela variável fixed_key. Ela possui exatamente 32 bytes, o que corresponde ao AES-256, uma versão de 256 bits do algoritmo AES.

- Vetor de Inicialização (IV):
O código utiliza um vetor de inicialização (IV) fixo de 16 bytes com valor zero (iv = bytes([0] * 16)), o que compromete a segurança, pois IVs fixos podem tornar o algoritmo vulnerável a ataques de texto conhecido.

- Modo de Operação:
O modo CBC (Cipher Block Chaining) é utilizado, que requer um IV para garantir a aleatoriedade da saída, mesmo para entradas repetidas.

- Preenchimento de Dados (Padding):
O código utiliza o esquema de padding PKCS7, que ajusta o tamanho do texto de entrada para que seja múltiplo do tamanho do bloco AES (16 bytes).

É importante observar que essa abordagem facilita a integridade dos dados criptografados, mas pode comprometer a segurança devido ao uso de uma chave e IV estáticos.
