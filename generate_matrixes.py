import os
import pickle

from create_sparse_matrix_traditional import create_sparse_matrix_traditional
from algorithm_1_hash import Sparse_matrix_hash
from algorithm_2_AVL import Sparse_matrix_AVL


# ------------------ parâmetros que você pode mudar ------------------ #

# valores de i (matriz 10^i x 10^i)
I_VALUES = range(2, 6)   # i = 2 -> 100x100. Ajuste aqui se quiser mais.

OUTPUT_DIR = "matrices"  # pasta onde os arquivos serão salvos


# ------------------------- funções auxiliares ------------------------ #

def sparsities_for_i(i):
    """Mesmo esquema do benchmark: esparsidades dependem de i."""
    if i >= 4:
        return [1 / 10 ** (i + 2), 1 / 10 ** (i + 1), 1 / 10 ** i]
    else:
        return [0.01, 0.05, 0.1, 0.2]


def format_sparsity(s):
    """Transforma a sparsity em string segura para nome de arquivo."""
    # 0.01 -> "0_01"
    return str(s).replace('.', '_')


# ----------------------------- principal ----------------------------- #

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i in I_VALUES:
        sparsities = sparsities_for_i(i)

        for sparsity in sparsities:
            print(f"Gerando matrizes para i={i}, sparsity={sparsity}...")

            # matrizes tradicionais A e B
            A_trad = create_sparse_matrix_traditional(i, sparsity)
            B_trad = create_sparse_matrix_traditional(i, sparsity)

            # representações esparsas
            A_hash = Sparse_matrix_hash(A_trad)
            B_hash = Sparse_matrix_hash(B_trad)

            A_avl = Sparse_matrix_AVL(A_trad)
            B_avl = Sparse_matrix_AVL(B_trad)

            # empacota tudo em um dicionário
            data = {
                "i": i,
                "sparsity": sparsity,
                "shape": (len(A_trad), len(A_trad[0])),
                "A_trad": A_trad,
                "B_trad": B_trad,
                "A_hash": A_hash,
                "B_hash": B_hash,
                "A_avl": A_avl,
                "B_avl": B_avl,
            }

            # nome do arquivo
            fname = f"matrices_i{i}_s{format_sparsity(sparsity)}.pkl"
            path = os.path.join(OUTPUT_DIR, fname)

            # salva com pickle
            with open(path, "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

            print(f"  -> salvo em {path}")

    print("\nTerminou de gerar todas as matrizes.")


if __name__ == "__main__":
    main()
