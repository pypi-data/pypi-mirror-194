

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def insert_node(node, value):
    if value < node.value:
        if node.left:
            insert_node(node.left, value)
        else:
            node.left = Node(value)
    else:
        if node.right:
            insert_node(node.right, value)
        else:
            node.right = Node(value)


def print_tree(node, prefix="", is_left=True):
    if not node:
        print("Empty Tree")
        return

    if node.right:
        print_tree(node.right, prefix + ("│   " if is_left else "    "), False)

    print(prefix + ("└── " if is_left else "┌── ") + str(node.value))

    if node.left:
        print_tree(node.left, prefix + ("    " if is_left else "│   "), True)



