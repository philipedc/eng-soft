
class Node: 

  def __init__(self, key):
    self.key = key
    self.value = None
    self.children = []

class Tree:
  def __init__(self, key=''):
    self.root = Node(key)
  
  def compare(self, str1, str2):
    # return the number of coincident characters
    matches = 0
    total_comparisions = min(len(str1), len(str2))

    for idx in range(total_comparisions):
      if (str1[idx] != str2[idx]):
        break
      else:
        matches += 1
    
    return matches

  def insert(self, node, father=None):
    # return only newly created node

    if (not father):
      father = self.root

    # check if there's a common prefix
    matches = 0
    child = None
    for child_local in father.children:
      matches_local = self.compare(child_local.key, node.key)
      if matches_local > matches:
        matches = matches_local
        child = child_local

    if matches > 0:
      # case 1: child's node is fully matched, but the current key has more characters
      if matches == len(child.key):
        diff_char = node.key[matches:]
        new_node = Node(diff_char)
        new_node.value = node.value
        return self.insert(new_node, child)
      
    # case 2: child's node is a prefix but doesn't fully match the current key
      if matches < len(child.key):

        common_prefix = child.key[0:matches]
        intermediary_node = Node(common_prefix)

        father.children.remove(child)
        father.children.append(intermediary_node)

        old_node = Node(child.key[matches:])
        old_node.value = child.value
        intermediary_node.children.append(old_node)

        new_node = Node(node.key[matches:])
        new_node.value = node.value
        intermediary_node.children.append(new_node)

        print(f"{child.key} with {node.key} broke into {old_node.key} <- {common_prefix} -> {new_node.key} ")
        return new_node
      
    father.children.append(node)
    return node

  def remove(self, key, node=None):
    if not node:
      node = self.root

    matches = 0
    child = None
    for child_local in node.children:
      matches_local = self.compare(child_local.key, key)
      if matches_local > matches:
        matches = matches_local
        child = child_local

    if matches == 0:
        return

    diff = key[matches:]
    if diff == '':
      if child.children == []:
        node.children.remove(child)
      else:
        child.value = None
    self.remove(diff, child)

  def print(self, root, depth=0):
    
    print("|" * depth + root.key + ": " + str(root.value))
    for child in root.children:
      self.print(child, depth + 1)

  def __getitem__(self, key, node=None):
    if not node:
      node = self.root

    key = str(key)

    matches = 0
    child = None
    for child_local in node.children:
      matches_local = self.compare(child_local.key, key)
      if matches_local > matches:
        matches = matches_local
        child = child_local

    if matches == 0:
        return None

    diff = key[matches:]
    if diff == '':
        return child.value
    
    return self.__getitem__(diff, child)


class Trie(Tree):
  def __init__(self):

    super().__init__()
    self.reverse_tree = Tree()


  def add(self, key, idx):
    new_node = Node(key)
    new_node.value = str(idx)
    self.insert(new_node)

    new_node_reversed = Node(str(idx))
    new_node_reversed.value = key
    self.reverse_tree.insert(new_node_reversed)


tree = Trie()
# tree.add("0")
tree.add("0001", 10)
tree.add("1111", 20)
# tree.print(tree.root)
reverse_tree = tree.reverse_tree
print(reverse_tree[10])