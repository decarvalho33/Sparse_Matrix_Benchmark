from create_sparse_matrix_traditional import create_sparse_matrix_traditional

class Sparse_matrix_hash:

    def __init__(self, n_rows, n_cols, capacity=24, matrix_traditional= None):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.base_n_cols = n_cols
        self.capacity = capacity
        self.size = 0
        self.is_transposed = 0
        self.buckets = [[] for _ in range(self.capacity)]
    
        if matrix_traditional is not None:
            for i in range(n_rows):
                    for j in range(n_cols):
                        val = matrix_traditional[i][j]
                        if val != 0:
                            self.insert(i, j, val)

    def acess(self, i, j):
        if self.is_transposed:
            ib, jb = j, i
        else:
            ib, jb = i, j
        bucket_index, pos = self.find_entry(ib, jb)
        if pos is None:
            return 0.0
        return self.buckets[bucket_index][pos][2]


    def insert(self, i, j, x):
        if self.is_transposed:
            ib, jb = j, i
        else:
            ib, jb = i, j

        bucket_index, pos = self.find_entry(ib, jb)
        bucket = self.buckets[bucket_index]

        if x == 0.0:
            if pos is not None:
                bucket.pop(pos)   
                self.size -= 1    
            return
            
        if pos is None:
            #chave nova -> adiciona
            bucket.append([ib, jb, x])
            self.size += 1
        else:
            #chave já existe -> atualiza valor
            bucket[pos][2] = x

        return 
    
    def transpose(self):
        self.is_transposed=1 if self.is_transposed==0 else 0
        self.n_rows, self.n_cols = self.n_cols, self.n_rows
        return self
    
    def plus_matrix(self, B):
        P = Sparse_matrix_hash(self.n_rows, self.n_cols,
                               capacity=max(self.capacity, B.capacity))

        for i, j, val in self.items():
            P.insert(i, j, val)

        for i, j, val in B.items():
            atual = P.acess(i, j)
            P.insert(i, j, atual + val)

        return P
    
    def times_scalar(self, a):
        S = Sparse_matrix_hash(self.n_rows, self.n_cols,
                               capacity=self.capacity)

        for i, j, val in self.items():
            S.insert(i, j, a * val)

        return S
    
    def times_matrix(self, B):

        T = Sparse_matrix_hash(self.n_rows, B.n_cols,
                               capacity=max(self.capacity, B.capacity))

        A_items = list(self.items())
        B_items = list(B.items())

        for i, j, a_val in A_items:
            for i2, k, b_val in B_items:
                if i2 == j:
                    atual = T.acess(i, k)
                    T.insert(i, k, atual + a_val * b_val)

        return T
# ---------------------- aux functions

    def hash(self, i, j):
        return (i*self.base_n_cols+j) % self.capacity

    def find_entry(self, ib, jb):
        bucket_index = self.hash(ib, jb)
        bucket = self.buckets[bucket_index]

        #verificar valor da chave com o índice original, dentro do bucket
        pos = 0
        for (i2, j2, _) in bucket:
            if i2 == ib and j2 == jb:
                return bucket_index, pos
            pos+=1
        return bucket_index, None
    
    def items(self):
        for bucket in self.buckets:
            for ib, jb, val in bucket:
                if self.is_transposed:
                    yield jb, ib, val
                else:
                    yield ib, jb, val