import matplotlib.pyplot as plt
import timeit

for i in range(2, 6):
    if i >= 4:
        sparcities = [1/10**(i+2), 1/10**(i+1), 1/10**i]
    else:
        sparcities = [0.01, 0.05, 0.1, 0.2]
    
    hash_times = []
    avl_times = []
    
    for sparcity in sparcities:
        setup_code = f"""
from create_sparse_matrix_traditional import create_sparse_matrix_traditional
#from algorithm_1_hash.py import Sparse_matrix_hash
from algorithm_2_AVL import Sparse_matrix_AVL

trad_A = create_sparse_matrix_traditional({i}, 0.01)
trad_B = create_sparse_matrix_traditional({i}, 0.01)

A_avl = Sparse_matrix_AVL(trad_A)
B_avl = Sparse_matrix_AVL(trad_B)

#A_hash = Sparse_matrix_hash(trad_A)
#B_hash = Sparse_matrix_hash(trad_A)
        """

        benchmark_hash = """
B_avl[50, 50] = 1
        """

        benchmark_avl = """
A_avl[50, 50] = 1
        """

        execution_time_hash = timeit.repeat(stmt=benchmark_avl, setup=setup_code, number=10000, repeat=1)
        hash_times.append(execution_time_hash[0])
        
        execution_time_avl = timeit.repeat(stmt=benchmark_avl, setup=setup_code, number=10000, repeat=1)
        avl_times.append(execution_time_avl[0])

    plt.figure(figsize=(8,5))
    plt.plot(sparcities, avl_times, marker='o', label='AVL')
    plt.plot(sparcities, hash_times, marker='s', label='Hash')
    plt.xlabel('Sparsity')
    plt.ylabel('Execution Time (s)')
    plt.title(f"Execução de Inserção (i={i})")
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.tight_layout()
    plt.savefig(f'insertion_i{i}.png')