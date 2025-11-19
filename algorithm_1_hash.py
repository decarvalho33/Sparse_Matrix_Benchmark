from create_sparse_matrix_traditional import create_sparse_matrix_traditional

class Sparse_matrix_hash:

    def __init__(self, capacity=24):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def hash(self, i, j):
        return i+j % self.capacity

    def acess_element(self, i, j):
        index = self.Hash(self, i, j)
        return index
    
