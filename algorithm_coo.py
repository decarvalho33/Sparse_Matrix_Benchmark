from create_sparse_matrix_traditional import create_sparse_matrix_traditional

class SparseMatrixCOO:
    def __init__(self):
        self.data_vec = []
        self.col_vec = []
        self.row_vec = []
        self.data_len = 0
        self.cols_len = 0
        self.rows_len = 0

    def transform_sparse_matrix(self, A):
        self.rows_len = len(A)
        self.cols_len = len(A[0])
        self.data_vec = []
        self.col_vec = []
        self.row_vec = []
        for i in range(self.rows_len):
            for j in range(self.cols_len):
                if A[i][j] != 0:
                    self.data_vec.append(A[i][j])
                    self.row_vec.append(i)
                    self.col_vec.append(j)
        self.data_len = len(self.data_vec)

    def find_index(self, row, col):
        left = 0
        right = self.data_len
        
        while left < right:
            mid = (left + right) // 2
            mid_pair = (self.row_vec[mid], self.col_vec[mid])
            if mid_pair < (row, col):
                left = mid + 1
            else:
                right = mid
        return left
    
    def add_element(self, element_data, element_col, element_row):
        i = self.find_index(element_row, element_col)
        if i < self.data_len and self.row_vec[i] == element_row and self.col_vec[i] == element_col:
            self.data_vec[i] = element_data
        else:
            self.data_vec.insert(i, element_data)
            self.row_vec.insert(i, element_row)
            self.col_vec.insert(i, element_col)
    
    def get_element(self, element_row, element_col):
        i = self.find_index(element_row, element_col)
        if i < self.data_len and self.row_vec[i] == element_row and self.col_vec[i] == element_col:
            return self.data_vec[i]
        return 0
    
    def transpose_matrix(self):
        return self.col_vec, self.row_vec
    '''
    def matrix_sum(self, data_vecB, row_vecB, col_vecB):
        len_b = len(data_vecB)
        data_vecC, row_vecC, col_vecC = [0]*(self.data_len + len_b), [0]*(self.data_len + len_b), [0]*(self.data_len + len_b)
        for i in range(len_b):
            index = self.get_element(row_vecB[i], col_vecB[i])
    '''     


A = create_sparse_matrix_traditional(5, 0.2)

print(A)
print(transform_to_csr(A))