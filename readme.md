## Introdução

A Trie (ou Árvore de Prefixos) é uma estrutura de dados para armazenar strings e realizar operações como inserções, buscas e remoções. A principal característica é a capacidade de armazenar strings de forma compacta e eficiente. É bastante útil em operações de prefix matching (como visto em sala) ou em sistemas de recomendação baseados em prefixo.

## Detalhes de Implementação:

O detalhe que mais gerou dificuldade na criação da estrutura para apoiar o algoritmo LZW foi que a árvore deveria ser capaz de pesquisar pela chave ou pelo valor (tree[key] = value ou tree[value] = key). A solução adotada (talvez não seja a melhor) foi criar duas árvores e adicionar a chave e o valor invertidos.


## Testes/Benchmark

Testes foram criados para garantir que a árvore funciona como o esperado após cada alteração: `python3 test_tree.py`. 