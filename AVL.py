class node:
    def __init__(self, key, value):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.value = value

def get_height(node):
    if not node:
        return 0
    return node.height

def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)

def right_rotate(y):
    x = y.left
    T2 = x.right

    # Rotação
    x.right = y
    y.left = T2

    # Atualiza heights
    y.height = max(get_height(y.left), get_height(y.right)) + 1
    x.height = max(get_height(x.left), get_height(x.right)) + 1

    return x

def left_rotate(x):
    y = x.right
    T2 = y.left

    # Rotação
    y.left = x
    x.right = T2

    # Atualiza heights
    x.height = max(get_height(x.left), get_height(x.right)) + 1
    y.height = max(get_height(y.left), get_height(y.right)) + 1

    return y

def balance(root):
    root.height = max(get_height(root.left), get_height(root.right)) + 1

    balance = get_balance(root)
    if balance > 1:
        if get_balance(root.left) >= 0:
            return right_rotate(root)
        else:
            root.left = left_rotate(root.left)
            return right_rotate(root)
    if balance < -1:
        if get_balance(root.right) <= 0:
            return left_rotate(root)
        else:
            root.right = right_rotate(root.right)
            return left_rotate(root)
    return root

def min_value_node(node):
    current = node
    while current.left:
        current = current.left
    return current

def in_order_elements(root):
        if not root:
            return []
        return in_order_elements(root.left) + [(root.key, root.value)] + in_order_elements(root.right)