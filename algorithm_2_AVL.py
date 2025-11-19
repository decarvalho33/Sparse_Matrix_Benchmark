from create_sparse_matrix_traditional import create_sparse_matrix_traditional

class AVL_node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class Sparse_matrix_AVL:

    def __init__(self):
        self.root = None