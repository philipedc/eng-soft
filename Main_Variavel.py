import LZW_Variavel
import argparse
import time

def calcular_taxa_compressao(tam_original, tam_comprimido):
    tam_comprimido = -(-tam_comprimido // 8)
    taxa_compressao = round(100-100*tam_comprimido/tam_original, 2)
    return taxa_compressao
    
def main():
    #Analisando os argumentos passados
    parser = argparse.ArgumentParser()
    parser.add_argument('arquivo_entrada', type=str)
    parser.add_argument('arquivo_comprimido', type=str)
    parser.add_argument('arquivo_descomprimido', type=str)
    parser.add_argument('--tam_max_dic', type=int, default=12)
    args = parser.parse_args()

    #Lendo o arquivo de entrada
    with open(args.arquivo_entrada, 'rb') as file:
        dados_entrada = file.read()
    tam_entrada = len(dados_entrada)

    #Comprimindo os dados
    tempo_inicial_compressao = time.time()
    codigos_compessao, mudancas_tam = LZW_Variavel.lzw_compressor(dados_entrada, args.tam_max_dic)
    tempo_final_compressao = time.time()
    
    #Convertendo os códigos de compressão para binário e concatenando tudo em uma única string binária
    string_bin_comp = LZW_Variavel.converter_para_string_binaria(codigos_compessao, mudancas_tam)
    
    #Convertendo a string binária para bytes e salvando em um arquivo
    LZW_Variavel.salvar_bits_em_arquivo(args.arquivo_comprimido, string_bin_comp)
    
    #Transformando os bytes do arquivo comprimido em uma string binária
    string_bin_descomp = LZW_Variavel.ler_bytes_de_arquivo(args.arquivo_comprimido)
    
    #Convertendo a string binária de volta para códigos de compressão
    codigos_descompressao = LZW_Variavel.converter_string_binaria_para_codigos(string_bin_descomp, mudancas_tam)
    
    #Descomprimindo os códigos de compressão
    tempo_inicial_descompressao = time.time()
    arquivo_descomprimido = LZW_Variavel.lzw_descompressor(codigos_descompressao, args.tam_max_dic)
    tempo_final_descompressao = time.time()
   
    #Salvando o arquivo descomprimido
    with open(args.arquivo_descomprimido, 'wb') as file:
        file.write(arquivo_descomprimido)

    #Calculando a taxa de compressão
    taxa_compressao = calcular_taxa_compressao(tam_entrada, len(string_bin_comp))
    print(f'Taxa de compressão = {taxa_compressao}%')

    print(f'Tempo de compressão = {1000*(tempo_final_compressao - tempo_inicial_compressao):.2f} ms')

    print(f'Tempo de descompresão = {1000*(tempo_final_descompressao - tempo_inicial_descompressao):.2f} ms')


if __name__ == "__main__":
    tempo_inicial = time.time()
    main()
    tempo_final = time.time()
    print(f'Tempo total de execução = {1000*(tempo_final - tempo_inicial):.2f} ms')
