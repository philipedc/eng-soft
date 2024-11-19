import tree

def lzw_compressor(texto_original, tam_codigo=12):
    tam_max_dic = 2**tam_codigo
    tam_dic = 256
    dicionario = tree.Trie()
    for i in range(tam_dic):
        dicionario.add(chr(i), str(i))
    palavra_atual = b""
    texto_comprimido = []

    for c in texto_original:
        prox_palavra = palavra_atual + bytes([c])
        if dicionario[prox_palavra.decode('latin1')] is not None:
            palavra_atual = prox_palavra
        else:
            texto_comprimido.append(int(dicionario[palavra_atual.decode('latin1')]))

            if tam_dic < tam_max_dic:
                dicionario.add(prox_palavra.decode('latin1'), str(tam_dic))
                tam_dic += 1
            else:
                dicionario = tree.Trie()
                tam_dic = 256
                for i in range(tam_dic):
                    dicionario.add(chr(i), str(i))
                
            palavra_atual = bytes([c])

    if palavra_atual:
        texto_comprimido.append(int(dicionario[palavra_atual.decode('latin1')]))

    return texto_comprimido

def lzw_descompressor(texto_comprimido, tam_codigo=12):
    tam_dic = 256
    dicionario = tree.Trie()
    for i in range(tam_dic):
        dicionario.add(str(i), chr(i))
    tam_max_dic = 2**tam_codigo
    
    texto_comprimido = iter(texto_comprimido)
    palavra_atual = chr(next(texto_comprimido)).encode('latin1')
    texto_descomprimido = [palavra_atual]

    for k in texto_comprimido:
        if dicionario[str(k)] is not None:
            codigo = dicionario[str(k)].encode('latin1')
        else:
            codigo = palavra_atual + bytes([palavra_atual[0]])
        texto_descomprimido.append(codigo)

        if tam_dic < tam_max_dic:
            dicionario.add(str(tam_dic), (palavra_atual + bytes([codigo[0]])).decode('latin1'))
            tam_dic += 1
        else:
            dicionario = tree.Trie()
            for i in range(256):
                dicionario.add(str(i), chr(i))
            tam_dic = 256

        palavra_atual = codigo
    
    return b''.join(texto_descomprimido)

def converter_para_string_binaria(codigos, tam_codigo=12):
    # Converte os códigos de compressão para binário e concatena tudo em uma única string binária
    dados_binarios = ''.join(format(codigo, f'0{tam_codigo}b') for codigo in codigos)
    return dados_binarios

def salvar_bits_em_arquivo(nome_arquivo, dados_binarios):
    # Adiciona zeros ao final da string binária para que ela tenha um número inteiro de bytes
    correcao_de_bytes = len(dados_binarios) % 8
    
    if correcao_de_bytes != 0:
        dados_binarios = dados_binarios.ljust(len(dados_binarios) + (8 - correcao_de_bytes), '0')
    
    # Agrupa a string binária em bytes e salva no arquivo
    dados_bytes = [dados_binarios[i:i+8] for i in range(0, len(dados_binarios), 8)]
    
    # Escreve os bytes no arquivo
    with open(nome_arquivo, 'wb') as f:
        for byte in dados_bytes:
            f.write(bytes([int(byte, 2)]))  # Converte o byte de binário para inteiro e escreve no arquivo

def ler_bytes_de_arquivo(nome_arquivo):
    # Lê os bytes do arquivo
    with open(nome_arquivo, 'rb') as f:
        dados_bytes = f.read()

    # Converte os bytes para uma string binária
    string_binaria = ''.join(format(byte, '08b') for byte in dados_bytes)

    return string_binaria

def converter_string_binaria_para_codigos(dados_binarios, tam_codigo=12): 
    ind = 0
    codigos = []
    while ind < len(dados_binarios):
        # Teste para ignorar os bits extras no final da string binária
        if ind+tam_codigo <= len(dados_binarios):
            codigo_binario = dados_binarios[ind:ind + tam_codigo]
            codigo_atual = int(codigo_binario, 2)
            codigos.append(codigo_atual)
         
        ind += tam_codigo
    return codigos

def print_lzw_codes(string_binaria, arquivo_aux, tam_codigo=12):
    ind = 0
    codigos = []
    while ind < len(string_binaria):
        codigo_binario = string_binaria[ind:ind + tam_codigo]
        codigo_atual = int(codigo_binario, 2)
        codigos.append(codigo_atual)
         
        ind += tam_codigo
    
    with open(arquivo_aux, 'w') as file:
        for codigo in codigos:
            file.write(f"{codigo}\n")
