import os
import pickle
import random

from create_sparse_matrix_traditional import create_sparse_matrix_traditional
from algorithm_1_hash import Sparse_matrix_hash
from algorithm_2_AVL import Sparse_matrix_AVL

OUTPUT_DIR = "matrices"  # Pasta para salvar arquivos

I_VALUES = range(2, 6)

def sparsities_for_i(i):
    if i >= 4:
        return [1 / 10 ** (i + 2), 1 / 10 ** (i + 1), 1 / 10 ** i]
    else:
        return [0.01, 0.05, 0.1, 0.2]

def format_sparsity(s):
    return str(s).replace('.', '_')

# Gera matriz AVL direto sem passar por tradicional
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

# Gera matriz Hash direto sem passar por tradicional
def create_sparse_matrix_hash(i, sparsity):
    size = 10**i
    total_elements = size * size
    nonzeros = int(total_elements * sparsity)
    hash_matrix = Sparse_matrix_hash(capacity=24)
    hash_matrix.n_rows = size
    hash_matrix.n_cols = size
    hash_matrix.base_n_cols = size
    positions = set()
    while len(positions) < nonzeros:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        positions.add((row, col))
    for (row, col) in positions:
        value = random.randint(1, 100)
        hash_matrix.insert(row, col, value)
    return hash_matrix

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i in I_VALUES:
        sparsities = sparsities_for_i(i)
        for sparsity in sparsities:
            print(f"Gerando matrizes para i={i}, sparsity={sparsity}...")

            shape = (10**i, 10**i)
            # Gera AVL e Hash diretamente
            A_avl = create_sparse_matrix_AVL(i, sparsity)
            B_avl = create_sparse_matrix_AVL(i, sparsity)
            A_hash = create_sparse_matrix_hash(i, sparsity)
            B_hash = create_sparse_matrix_hash(i, sparsity)

            # Opcional: Se quiser tradicional também, pode gerar (demora mais para grande)
            # A_trad = create_sparse_matrix_traditional(i, sparsity)
            # B_trad = create_sparse_matrix_traditional(i, sparsity)
            # else, use None
            A_trad = None
            B_trad = None

            data = {
                "i": i,
                "sparsity": sparsity,
                "shape": shape,
                "A_trad": A_trad,
                "B_trad": B_trad,
                "A_hash": A_hash,
                "B_hash": B_hash,
                "A_avl": A_avl,
                "B_avl": B_avl,
            }
            fname = f"matrices_i{i}_s{format_sparsity(sparsity)}.pkl"
            path = os.path.join(OUTPUT_DIR, fname)
            with open(path, "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"  -> salvo em {path}")
    print("\nTerminou de gerar todas as matrizes.")

if __name__ == "__main__":
    main()
