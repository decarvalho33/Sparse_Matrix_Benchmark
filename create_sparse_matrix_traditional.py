import numpy as np

def create_sparse_matrix_traditional(i, sparsity):
    rows = cols = 10 ** i
    
    # inicializa matriz totalmente zerada, mas "linha a linha"
    matrix = [[0.0 for _ in range(cols)] for _ in range(rows)]
    
    total = rows * cols
    non_zero = int(total * sparsity)

    # segurança: se sparsity for muito pequeno, não dá erro
    if non_zero == 0:
        return matrix

    # escolhe índices únicos
    indices = np.random.choice(total, non_zero, replace=False)

    # preenche os não zeros
    for idx in indices:
        r = idx // cols
        c = idx % cols
        matrix[r][c] = float(np.random.rand())
    
    return matrix
