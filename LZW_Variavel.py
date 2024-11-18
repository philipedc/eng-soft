import tree

def lzw_compressor(texto_original, tam_max_codigo=12):
    tam_max_dic = 2**tam_max_codigo
    tam_dic = 256
    dicionario = tree.Trie()
    for i in range(tam_dic):
        dicionario.add(chr(i), i)
    palavra_atual = ""
    texto_comprimido = []
    mudancas_tamanho = [] # Lista que armazena os indices onde o tamanho do código muda
    tam_codigo = 9

    for c in texto_original:
        prox_palavra = palavra_atual + c
        # Se a palavra atual + o próximo caractere estiver no dicionário, a palavra atual é atualizada
        if dicionario[prox_palavra] is not None:
            palavra_atual = prox_palavra
        # Se a palavra atual + o próximo caractere não estiver no dicionário, a palavra atual é adicionada ao dicionário
        else:
            texto_comprimido.append(int(dicionario[palavra_atual]))
            # Se o dicionário ainda não está cheio, a palavra atual + o próximo caractere é adicionada ao dicionário
            if tam_dic < tam_max_dic:
                dicionario.add(prox_palavra, tam_dic)
                tam_dic += 1
            # Se o dicionário está cheio, o dicionário é reinicializado com os 256 primeiros caracteres ASCII
            else:
                dicionario = tree.Trie()
                tam_dic = 256
                for i in range(tam_dic):
                    dicionario.add(chr(i), i)

            # Se o tamanho do dicionário é igual a 2^tamanho do código, o tamanho do código é incrementado
            if tam_dic == 2 ** (tam_codigo):
                tam_codigo += 1
                mudancas_tamanho.append(len(texto_comprimido))
            palavra_atual = c

    if palavra_atual:
        texto_comprimido.append(int(dicionario[palavra_atual]))

    return texto_comprimido, mudancas_tamanho

def lzw_descompressor(texto_comprimido, tam_codigo=12):
    
    tam_max_dic = 2**tam_codigo
    tam_dic = 256
    dicionario = tree.Trie()
    for i in range(tam_dic):
        dicionario.add(str(i), chr(i))
    tam_codigo = 9
    texto_comprimido = iter(texto_comprimido) # Transforma a lista de códigos em um iterador
    palavra_atual = chr(next(texto_comprimido)) # Pega o primeiro código e transforma em caractere
    texto_descomprimido = [palavra_atual]
    
    for k in texto_comprimido:
        # Se o código está no dicionário, a palavra atual é atualizada
        if k < tam_dic:
            codigo = dicionario[k]
        # Se o código não está no dicionário, a palavra atual é atualizada com o primeiro caractere da palavra atual
        elif k == tam_dic:
            codigo = palavra_atual + palavra_atual[0]
        # Se o código é inválido, uma exceção é lançada
        else:
            raise ValueError(f"Codigo comprimido invalido: {k}")
        
        texto_descomprimido.append(codigo)
        
        # Se o dicionário ainda não está cheio, a palavra atual + o primeiro caractere da palavra atual é adicionada ao dicionário
        if tam_dic < tam_max_dic:
            dicionario.add(str(tam_dic), palavra_atual + codigo[0])
            tam_dic += 1
        # Se o dicionário está cheio, o dicionário é reinicializado com os 256 primeiros caracteres
        else:
            dicionario = tree.Trie()
            for i in range(256):
                dicionario.add(str(i), chr(i))
            tam_dic = 256
        
        # Se o tamanho do dicionário é igual a 2^tamanho do código, o tamanho do código é incrementado
        if tam_dic == 2 ** tam_codigo:
            tam_codigo += 1
        
        palavra_atual = codigo
    
    return ''.join(texto_descomprimido)

def converter_para_string_binaria(codigos, mudancas_tam):
    
    dados_binarios = ""
    tam_codigo = 9
    indice_mudanca = 0
    
    # Itera sobre os códigos e os converte para binário
    for i, codigo in enumerate(codigos):
        if indice_mudanca < len(mudancas_tam) and i == mudancas_tam[indice_mudanca]:
            tam_codigo += 1
            indice_mudanca += 1

        dados_binarios += format(codigo, f'0{tam_codigo}b')
    
    return dados_binarios

def salvar_bits_em_arquivo(arquivo_comprimido, string_binaria):
    # Adiciona zeros ao final da string binária para que ela tenha um número inteiro de bytes
    correcao_de_bytes = len(string_binaria) % 8
    if correcao_de_bytes != 0:
        string_binaria = string_binaria.ljust(len(string_binaria) + (8 - correcao_de_bytes), '0')
    
    # Converte a string binária para bytes
    dados_em_bytes = bytearray()
    for i in range(0, len(string_binaria), 8):
        byte = string_binaria[i:i + 8]
        dados_em_bytes.append(int(byte, 2))

    with open(arquivo_comprimido, 'wb') as file:
        file.write(dados_em_bytes)
    
def ler_bytes_de_arquivo(nome_arquivo):
    # Lê os bytes do arquivo
    with open(nome_arquivo, 'rb') as f:
        dados_bytes = f.read()

    # Converte os bytes para uma string binária
    string_binaria = ''.join(format(byte, '08b') for byte in dados_bytes)

    return string_binaria

def converter_string_binaria_para_codigos(dados_binarios, mudancas_tam):
    tam_codigo = 9
    indice_mud = 0
    ind = 0
    codigos = []

    # Itera sobre a string binária e a converte para códigos
    while ind < len(dados_binarios):
        if indice_mud < len(mudancas_tam) and len(codigos) == mudancas_tam[indice_mud]:
            tam_codigo += 1
            indice_mud += 1
        
        # Teste para ignorar os bits extras no final da string binária
        if ind+tam_codigo <= len(dados_binarios):
            codigo_binario = dados_binarios[ind:ind + tam_codigo]
            codigo_atual = int(codigo_binario, 2)
            codigos.append(codigo_atual)
         
        ind += tam_codigo
    
    return codigos

def print_lzw_codes(string_binaria, arquivo_aux, mudancas_tam):
    tam_codigo = 9
    indice_mud = 0
    ind = 0
    codigos = []

    while ind < len(string_binaria):
        if indice_mud < len(mudancas_tam) and len(codigos) == mudancas_tam[indice_mud]:
            tam_codigo += 1
            indice_mud += 1
        
        codigo_binario = string_binaria[ind:ind + tam_codigo]
        codigo_atual = int(codigo_binario, 2)
        codigos.append(codigo_atual)
         
        ind += tam_codigo
    
    with open(arquivo_aux, 'w') as file:
        for codigo in codigos:
            file.write(f"{codigo}\n")  # Write each code as a new line

