import matplotlib.pyplot as plt
import timeit
import csv

OP = "Multiplicação"

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
        setup_code = f"""
from create_sparse_matrix_traditional import create_sparse_matrix_traditional
from algorithm_1_hash.py import Sparse_matrix_hash
from algorithm_2_AVL import Sparse_matrix_AVL

rows = cols = pow(10, i)
trad_A = create_sparse_matrix_traditional({i}, {sparcity})
trad_B = create_sparse_matrix_traditional({i}, {sparcity})

A_avl = Sparse_matrix_AVL(trad_A)
B_avl = Sparse_matrix_AVL(trad_B)

A_hash = Sparse_matrix_hash(trad_A)
B_hash = Sparse_matrix_hash(trad_A)
        """

        benchmark_hash = """
C_hash = A_hash.times_matrix(B_hash)
        """

        benchmark_avl = """
C_avl = A_avl * B_avl
        """

        benchmark_trad = """
trad_C = []
for c in range(cols):
    trad_C.append(([0.0] * rows))
for i in range(0, rows):
    for j in range(0, cols):
        C[i][j] = 0
        for k in range(0, cols):
            C[i][j] += A[i][k] * B[k][j]

        """

        execution_time_hash = timeit.repeat(stmt=benchmark_hash, setup=setup_code, number=10000, repeat=1)
        hash_times.append(execution_time_hash[0])
        
        execution_time_avl = timeit.repeat(stmt=benchmark_avl, setup=setup_code, number=10000, repeat=1)
        avl_times.append(execution_time_avl[0])
        
        execution_time_trad = timeit.repeat(stmt=benchmark_trad, setup=setup_code, number=10000, repeat=1)
        trad_times.append(execution_time_trad[0])

        dados.append([i, sparcity, execution_time_hash[0], execution_time_avl[0], execution_time_trad[0]])

    plt.figure(figsize=(8,5))
    plt.plot(sparcities, hash_times, marker='o', label='Hash')
    plt.plot(sparcities, avl_times, marker='s', label='AVL')
    plt.plot(sparcities, avl_times, marker='.', label='Trad')
    plt.xlabel('Sparsity')
    plt.ylabel('Execution Time (s)')
    plt.title(f"Execução de {OP} (i={i})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{OP}_i_{i}.png')


with open(f'Tempos_{OP}.csv', mode='w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    writer.writerow(['i', 'sparsity', 'hash_time', 'avl_time', 'trad_time'])
    writer.writerows(dados)