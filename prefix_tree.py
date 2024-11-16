# compact prefix tree

global_idx = 0

class Node: 
  value = None
  children = None  
  idx = None

  def __init__(self, value):
    self.value = value
    self.children = []

class Prefix_Tree:
  root = None
  
  def __init__(self, word=""):
    self.root = Node(word)
  
  def compare(self, str1, str2):
    # return the number of characters matched
    matches = 0
    total_comparisions = min(len(str1), len(str2))
    for idx in range(total_comparisions):
      if (str1[idx] != str2[idx]):
        return matches
      matches += 1
    return matches


  def insert(self, value, node=None):
    if not node:
      node = self.root
    if not value:
      return
    print(f"Inserting {value} in {node.value}")

    # check if there's a common prefix
    matches = 0
    child = None
    for child_local in node.children:
      matches_local = self.compare(child_local.value, value)
      if matches_local > matches:
        matches = matches_local
        child = child_local
    
    if matches > 0:
      # case 1: child's node is fully matched, but the current value has more characters
      if matches == len(child.value):
        diff_char = value[matches:]
        self.insert(diff_char, child)
        return 
      
      # case 2: child's node is a prefix but doesn't fully match the current value
      if matches < len(child.value):

        common_prefix = child.value[0:matches]
        intermediary_node = Node(common_prefix)

        node.children.remove(child)
        node.children.append(intermediary_node)

        old_node = Node(child.value[matches:])
        old_node.idx = child.idx
        intermediary_node.children.append(old_node)

        new_node = Node(value[matches:])
        self.assign_idx(new_node)
        intermediary_node.children.append(new_node)

        print(f"{child.value} with {value} broke into {old_node.value} <- {common_prefix} -> {new_node.value} ")
        return
          
    new_node = Node(value)
    self.assign_idx(new_node)
    node.children.append(new_node)
    return 
          

  def remove(self, value, node=None):
    if not node:
      node = self.root

    matches = 0
    child = None
    for child_local in node.children:
      matches_local = self.compare(child_local.value, value)
      if matches_local > matches:
        matches = matches_local
        child = child_local

    if matches == 0:
        return

    diff = value[matches:]
    if diff == '':
      if child.children == []:
        node.children.remove(child)
      else:
        child.idx = None
    self.remove(diff, child)

  def assign_idx(self, node):
    global global_idx
    node.idx = global_idx
    global_idx += 1
       
  def print(self, root, depth=0):
    
    print("|" * depth + root.value + ": " + str(root.idx))
    for child in root.children:
      self.print(child, depth + 1)


tree = Prefix_Tree()
tree.insert("a")
tree.insert("ate")
tree.insert("are")
tree.insert("be")
tree.insert("sit")
tree.insert("so")
tree.print(tree.root)
tree.remove("ate")
tree.print(tree.root)
