class node:    
    def __init__(self, value = ""):
        self.value = value
        self.branches = []

    def add_node(self, node):
        self.branches.append(node)

    
class Leaf(node):
    def __init__(self, p, q):
        self.p = p
        self.q = q
   
    def add_node(self, node):
        raise

        
class Tree(node):
    def __init__(self):
        super().__init__()
        


def visualise(tree, l = []):
    layer = []
    for b in tree.branches:

        if type(b) == Leaf:
            layer.append((b.p, b.q))
        else:
            layer.append((b.value, visualise(b, layer)))
            
    return layer