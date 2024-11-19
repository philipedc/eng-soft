## Introdução

A Trie (ou Árvore de Prefixos) é uma estrutura de dados eficiente para armazenar strings e realizar operações como inserções, buscas e remoções. Sua principal vantagem é a capacidade de armazenar strings de forma compacta e otimizada, tornando-a ideal para aplicações de prefix matching (como demonstrado em sala de aula) e sistemas de recomendação baseados em prefixos. As operações de inserção, busca e remoção na Trie têm complexidade O(n), onde n é o tamanho da string envolvida, já que é necessário percorrer os caracteres da string na árvore.

## Detalhes de Implementação:

Para otimizar o uso de memória, implementamos uma Trie compacta, ou seja, buscamos armazenar o máximo possível de caracteres em cada nó, evitando a criação de nós desnecessários.

Um dos principais desafios na implementação dessa estrutura foi adaptá-la para apoiar o algoritmo LZW (Lempel-Ziv-Welch). Especificamente, a Trie precisava ser capaz de realizar buscas tanto por chave quanto por valor (isto é, tree[key] = value ou tree[value] = key). Para resolver esse problema, criamos duas árvores: uma armazenando as chaves e outra armazenando os valores invertidos (onde cada valor é a chave na segunda árvore). Isso permite realizar buscas eficientes tanto por chave quanto por valor.


## Testes/Benchmark

Diversos testes foram desenvolvidos para garantir que a Trie funcione corretamente após cada modificação. Os testes podem ser executados com o comando: `python3 test_tree.py`.

Além disso, o algoritmo LZW foi comparado utilizando tanto o dicionário baseado na Trie quanto a estrutura de dados **dict** do Python, que utiliza uma **tabela hash**. Como esperado, a tabela hash apresentou desempenho superior, pois o caso médio de inserção e busca em uma tabela hash é O(1), enquanto na Trie é O(n), onde n é o tamanho das strings processadas.
