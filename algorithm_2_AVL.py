import AVL

class Sparse_matrix_AVL:
    def __init__(self, A=None):
        self.root = None
        self.transposed = False
        if not (A is None):
            self.transform_sparse_matrix(A)
    
    def __insert(self, root, key, value):
        if not root:
            return AVL.node(key, value)
        if key < root.key:
            root.left = self.__insert(root.left, key, value)
        elif key > root.key:
            root.right = self.__insert(root.right, key, value)
        else:
            root.value = value
            return root

        return AVL.balance(root)

    def __search_item(self, root, key):
        if not root:
            return 0
        if key < root.key:
            return self.__search_item(root.left, key)
        elif key > root.key:
            return self.__search_item(root.right, key)
        else:
            return root.value

    def __getitem__(self, key):
        if self.transposed:
            key = (key[1], key[0])
        return self.__search_item(self.root, key)
    
    def __setitem__(self, key, value):
        if self.transposed:
            key = (key[1], key[0])
        if value == 0:
            self.root = self.__delete(self.root, (key[0], key[1]))
        else:
            self.root = self.__insert(self.root, (key[0], key[1]), value)


    def __delete(self, root, key):
        if not root:
            return root
        if key < root.key:
            root.left = self.__delete(root.left, key)
        elif key > root.key:
            root.right = self.__delete(root.right, key)
        else:
            # Caso: um ou nenhum filho
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            # Caso: dois filhos
            temp = AVL.min_value_node(root.right)
            root.key = temp.key
            root.value = temp.value
            root.right = self.__delete(root.right, temp.key)
        if not root:
            return root
        
        AVL.balance(root)    
        return root
    

    def transpose(self):
        self.transposed = not self.transposed

    def __rmul__(self, other):
        if isinstance(other, Sparse_matrix_AVL):
            return self.__multiply_matrices(other)
        else:
            return self.__multiply_by_scalar(self.root, other)

    def __mul__(self, other):
        if isinstance(other, Sparse_matrix_AVL):
            return self.__multiply_matrices(other)
        else:
            return self.__multiply_by_scalar(self.root, other)

    def __multiply_matrices(self, other):
        C_tree = Sparse_matrix_AVL()

        A_elements = AVL.in_order_elements(self.root)
        B_elements = AVL.in_order_elements(other.root)
        
        for (i, ii), a_val in A_elements:
            for (jj, j), b_val in B_elements:
                if ii == jj:
                    C_val = C_tree[i, j]
                    value = C_val + a_val * b_val
                    C_tree[i, j] = value

        return C_tree


    def __multiply_by_scalar(self, root, scalar):
        if root is not None:
            root.value *= scalar
            self.__multiply_by_scalar(root.left, scalar)
            self.__multiply_by_scalar(root.right, scalar)


    def __add__(self, other):
        C_tree = Sparse_matrix_AVL()
        
        for (i, j), value in AVL.in_order_elements(self.root):
            C_tree[i, j] = value

        for (i, j), value in AVL.in_order_elements(other.root):
            current = C_tree[i, j]
            C_tree[i, j] = current + value

        return C_tree


    def transform_sparse_matrix(self, A):
        self.root = None
        for i in range(len(A)):
            for j in range(len(A[0])):
                valor = A[i][j]
                if valor != 0 and not isinstance(valor, list):
                    self.root = self.__insert(self.root, (i, j), A[i][j])


'''
def print_avl_tree(node, level=0):
    if node is not None:
        print('  ' * level + f'({node.key}) -> {node.value}')
        print_avl_tree(node.left, level + 1)
        print_avl_tree(node.right, level + 1)


trad_A = create_sparse_matrix_traditional(2, 1)
print("A = \n", trad_A)
trad_B = create_sparse_matrix_traditional(2, 1)
print("B = \n", trad_B)

A = Sparse_matrix_AVL(trad_A)
B = Sparse_matrix_AVL(trad_B)


#A[0, 0] = 1
#print_avl_tree(A.root)
#print_avl_tree(B.root)

C = A + B
#5 * A
print_avl_tree(C.root)
'''

import random

def create_sparse_matrix_AVL(i, sparsity):
    size = 10**i
    total_elements = size * size
    nonzeros = int(total_elements * sparsity)
    avl_matrix = Sparse_matrix_AVL()
    positions = set()
    while len(positions) < nonzeros:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        positions.add((row, col))
    for (row, col) in positions:
        value = random.randint(1, 100)
        avl_matrix[row, col] = value
    return avl_matrix