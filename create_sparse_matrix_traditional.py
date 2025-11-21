import numpy as np

def create_sparse_matrix_traditional(i, sparsity):
    rows = cols = pow(10, i)

    sparce_matrix = []
    for r in range(rows):
        sparce_matrix.append([0.0] * cols)
    
    total = rows * cols
    non_zero = int(total * sparsity)
    indices = np.random.choice(total, non_zero, replace=False)
    for index in indices:
        row = index // cols
        col = index % cols
        sparce_matrix[row][col] = np.random.rand()
    return sparce_matrix