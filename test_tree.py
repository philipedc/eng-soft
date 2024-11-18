import unittest
from tree import Trie
import time
import io
import sys


class TestTrie(unittest.TestCase):

    def setUp(self):
        # Configura uma instância do Trie para ser usada nos testes
        self.tree = Trie()
        self.tree.add("0001", 10)
        self.tree.add("1111", 20)

    def test_print_tree_format(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Executa o método print
        self.tree.print(self.tree.root)

        # Restaura saída padrão
        sys.stdout = sys.__stdout__

        # Verifica se a saída está correta
        expected_output = ": None\n|0001: 10\n|1111: 20\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

    
    def test_insert_and_retrieve(self):
        # Testa se os valores foram inseridos e recuperados corretamente
        self.assertEqual(self.tree.reverse_tree[10], "0001")
        self.assertEqual(self.tree.reverse_tree[20], "1111")

    
    def test_non_existent_key(self):
        # Testa tentativa de recuperar uma chave que não existe
        self.assertIsNone(self.tree[30])

    
    def test_remove_leaf_node(self):
        # Remove uma chave folha e verifica
        self.tree.remove("0001")
        self.assertIsNone(self.tree["0001"])
        self.assertEqual(self.tree.reverse_tree[20], "1111")

    
    def test_remove_internal_node(self):
        # Remove um nó que não é folha
        self.tree.add("111", 15)
        self.tree.remove("1111")
        self.assertIsNone(self.tree["1111"])
        self.assertEqual(self.tree.reverse_tree[15], "111")

    
    def test_reverse_tree(self):
        # Verifica se a árvore reversa está correta
        self.assertEqual(self.tree.reverse_tree[10], "0001")
        self.assertEqual(self.tree.reverse_tree[20], "1111")

    
    def test_insert_with_prefix(self):
        # Testa inserção de chave que é prefixo de outra
        self.tree.add("000", 30)
        self.assertEqual(self.tree.reverse_tree[30], "000")
        self.assertEqual(self.tree.reverse_tree[10], "0001")

    
    def test_insert_with_common_prefix(self):
        # Testa inserção de chave que compartilha prefixo
        self.tree.add("00012", 40)
        self.assertEqual(self.tree.reverse_tree[40], "00012")
        self.assertEqual(self.tree.reverse_tree[10], "0001")


if __name__ == "__main__":
    unittest.main()
