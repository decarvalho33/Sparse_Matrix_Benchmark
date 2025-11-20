import matplotlib.pyplot as plt
import timeit
import csv
import pickle

OP = "Inserção"

dados = []

for i in range(2, 7):
    if i >= 4:
        sparcities = [1/10**(i+2), 1/10**(i+1), 1/10**i]
    else:
        sparcities = [0.01, 0.05, 0.1, 0.2]
    
    hash_times = []
    avl_times = []
    trad_times = []
    
    for sparcity in sparcities:
        # monta o caminho do arquivo com base em i e sparsity
        sparcity_str = str(sparcity).replace('.', '_')
        matrix_file = f"matrices/matrices_i{i}_s{sparcity_str}.pkl"

        # ---------------------------------------------------------
        # SE i > 3 → NÃO carregar matriz tradicional
        # ---------------------------------------------------------
        if i > 3:
            setup_code = f"""
import pickle
from algorithm_1_hash import Sparse_matrix_hash
from algorithm_2_AVL import Sparse_matrix_AVL

with open(r"{matrix_file}", "rb") as f:
    data = pickle.load(f)

# Tradicional não carregada
trad_A = None
trad_B = None

A_hash = data["A_hash"]
B_hash = data["B_hash"]

A_avl = data["A_avl"]
B_avl = data["B_avl"]
            """

            benchmark_trad = "pass"   # NÃO medir tradição
        else:
            setup_code = f"""
import pickle
from algorithm_1_hash import Sparse_matrix_hash
from algorithm_2_AVL import Sparse_matrix_AVL

with open(r"{matrix_file}", "rb") as f:
    data = pickle.load(f)

trad_A = data["A_trad"]
trad_B = data["B_trad"]

A_hash = data["A_hash"]
B_hash = data["B_hash"]

A_avl = data["A_avl"]
B_avl = data["B_avl"]
            """

            benchmark_trad = """
trad_A[50][50] = 1
            """

        benchmark_hash = "A_hash.insert(50, 50, 1)"
        benchmark_avl  = "A_avl[50, 50] = 1"

        execution_time_hash = timeit.repeat(stmt=benchmark_hash, setup=setup_code, number=10000, repeat=1)
        hash_times.append(execution_time_hash[0])

        execution_time_avl = timeit.repeat(stmt=benchmark_avl, setup=setup_code, number=10000, repeat=1)
        avl_times.append(execution_time_avl[0])

        # ----------------------------------------------
        # SE i > 3, pula tradicional e usa valor nulo
        # ----------------------------------------------
        if i > 3:
            trad_time = None
        else:
            execution_time_trad = timeit.repeat(stmt=benchmark_trad, setup=setup_code, number=10000, repeat=1)
            trad_time = execution_time_trad[0]

        trad_times.append(trad_time)

        dados.append([i, sparcity, execution_time_hash[0], execution_time_avl[0], trad_time])

    plt.figure(figsize=(8,5))
    plt.plot(sparcities, hash_times, marker='o', label='Hash')
    plt.plot(sparcities, avl_times, marker='s', label='AVL')

    # só plota o tradicional se existir valores
    if any(x is not None for x in trad_times):
        plt.plot(sparcities, trad_times, marker='.', label='Trad')

    plt.xlabel('Sparsity')
    plt.ylabel('Execution Time (s)')
    plt.title(f"Execução de Inserção (i={i})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{OP}_i_{i}.png')


with open(f'Tempos_{OP}.csv', mode='w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    writer.writerow(['i', 'sparsity', 'hash_time', 'avl_time', 'trad_time'])
    writer.writerows(dados)
