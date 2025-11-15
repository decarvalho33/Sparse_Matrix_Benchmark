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
    
    def __getitem__(self, key):
        element_row = key[0]
        element_col = key[1]
        i = self.find_index(element_row, element_col)
        if i < self.data_len and self.row_vec[i] == element_row and self.col_vec[i] == element_col:
            return self.data_vec[i]
        return 0
    
    def transpose_matrix(self):
        return self.col_vec, self.row_vec

    def __add__(self, other):
        result = SparseMatrixCOO()
        i, j = 0, 0
        while i < len(self.data_vec) and j < len(other.data_vec):
            a_pos = (self.row_vec[i], self.col_vec[i])
            b_pos = (other.row_vec[j], other.col_vec[j])
            if a_pos == b_pos:
                value = self.data_vec[i] + other.data_vec[j]
                if value != 0:
                    result.row_vec.append(a_pos[0])
                    result.col_vec.append(a_pos[1])
                    result.data_vec.append(value)
                i += 1
                j += 1
            elif a_pos < b_pos:
                result.row_vec.append(self.row_vec[i])
                result.col_vec.append(self.col_vec[i])
                result.data_vec.append(self.data_vec[i])
                i += 1
            else:
                result.row_vec.append(other.row_vec[j])
                result.col_vec.append(other.col_vec[j])
                result.data_vec.append(other.data_vec[j])
                j += 1
        # Copie o que sobrou em cada matriz
        while i < len(self.data_vec):
            result.row_vec.append(self.row_vec[i])
            result.col_vec.append(self.col_vec[i])
            result.data_vec.append(self.data_vec[i])
            i += 1
        while j < len(other.data_vec):
            result.row_vec.append(other.row_vec[j])
            result.col_vec.append(other.col_vec[j])
            result.data_vec.append(other.data_vec[j])
            j += 1
        result.rows_len = self.rows_len
        result.cols_len = self.cols_len
        return result
    
    def show_matrix(self):
        print(f"Dimensões: ({self.rows_len}, {self.cols_len}) | Elementos não-zero: {self.data_len}")
        print("Dados:", self.data_vec)
        print("Linhas:", self.row_vec)
        print("Colunas:", self.col_vec)
        print("-" * 30)



trad_A = create_sparse_matrix_traditional(4, 0.2)
print("A = \n", trad_A)
trad_B = create_sparse_matrix_traditional(4, 0.2)
print("B = \n", trad_B)

A = SparseMatrixCOO()
A.transform_sparse_matrix(trad_A)
A.show_matrix()

print(A[1, 1])