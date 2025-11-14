import numpy as np

def create_sparse_matrix_traditional(i, sparsity):
    rows = cols = i#pow(10, i)

    sparce_matrix = np.zeros((rows, cols), dtype=np.float32)
    total = rows * cols
    non_zero = int(total * sparsity)
    indices = np.random.choice(total, non_zero, replace=False)
    for index in indices:
        row = index // cols
        col = index % cols
        sparce_matrix[row, col] = np.random.rand()
    return sparce_matrix
