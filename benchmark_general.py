import matplotlib.pyplot as plt
import timeit
import csv

dados = []

for i in range(2, 7):
    if i >= 4:
        sparcities = [1/10**(i+2), 1/10**(i+1), 1/10**i]
    else:
        sparcities = [0.01, 0.05, 0.1, 0.2]

    hash_times_a = []
    avl_times_a = []
    trad_times_a = []

    hash_times_s = []
    avl_times_s = []
    trad_times_s = []

    hash_times_i = []
    avl_times_i = []
    trad_times_i = []

    hash_times_t = []
    avl_times_t = []
    trad_times_t = []

    hash_times_m = []
    avl_times_m = []
    trad_times_m = []

    hash_times_e = []
    avl_times_e = []
    trad_times_e = []
    
    for sparcity in sparcities:

        setup_code = f"""
from create_sparse_matrix_traditional import create_sparse_matrix_traditional
from algorithm_1_hash import Sparse_matrix_hash, create_sparse_matrix_hash
from algorithm_2_AVL import Sparse_matrix_AVL, create_sparse_matrix_AVL
rows = cols = 10**{i}
if {i} < 4:
    trad_A = create_sparse_matrix_traditional({i}, {sparcity})
    trad_B = create_sparse_matrix_traditional({i}, {sparcity})

    A_avl = Sparse_matrix_AVL(trad_A)
    B_avl = Sparse_matrix_AVL(trad_B)

    A_hash = Sparse_matrix_hash(trad_A)
    B_hash = Sparse_matrix_hash(trad_B)
else:
    A_avl = create_sparse_matrix_AVL({i}, {sparcity})
    B_avl = create_sparse_matrix_AVL({i}, {sparcity})

    A_hash = create_sparse_matrix_hash({i}, {sparcity})
    B_hash = create_sparse_matrix_hash({i}, {sparcity})
        """
        

        OP = "Acesso"
        
        print(f'Executando {OP}, {i}, {sparcity}')

        benchmark_hash = """
A_hash.acess(0, 0)
        """

        benchmark_avl = """
A_avl[0, 0]
        """

        benchmark_trad = """
trad_A[0][0]
        """

        execution_time_hash = timeit.repeat(stmt=benchmark_hash, setup=setup_code, number=10000, repeat=1)
        hash_times_a.append(execution_time_hash[0])
        
        execution_time_avl = timeit.repeat(stmt=benchmark_avl, setup=setup_code, number=10000, repeat=1)
        avl_times_a.append(execution_time_avl[0])
        
        execution_time_trad = timeit.repeat(stmt=benchmark_trad, setup=setup_code, number=10000, repeat=1) if i < 4 else [0]
        
        trad_times_a.append(execution_time_trad[0])

        dados.append([OP, i, sparcity, execution_time_hash[0], execution_time_avl[0], execution_time_trad[0]])

        OP = 'Soma'



        benchmark_hash = """
C_hash = A_hash.plus_matrix(B_hash)
        """

        benchmark_avl = """
C_avl = A_avl + B_avl
        """

        benchmark_trad = """
trad_C = []
for c in range(cols):
    trad_C.append(([0.0] * rows))
for i in range(rows):
    for j in range(cols):
        trad_C[i][j] = trad_A[i][j] + trad_B[i][j]
        """
        print(f'Executando {OP}, {i}, {sparcity}')
        execution_time_hash = timeit.repeat(stmt=benchmark_hash, setup=setup_code, number=10000, repeat=1)
        hash_times_s.append(execution_time_hash[0])
        
        execution_time_avl = timeit.repeat(stmt=benchmark_avl, setup=setup_code, number=10000, repeat=1)
        avl_times_s.append(execution_time_avl[0])
        print(f'Executando {OP}, {i}, {sparcity}')
        
        execution_time_trad = timeit.repeat(stmt=benchmark_trad, setup=setup_code, number=10000, repeat=1) if i < 0 else [0]
        trad_times_s.append(execution_time_trad[0])
        print(f'Executando {OP}, {i}, {sparcity}')

        dados.append([OP, i, sparcity, execution_time_hash[0], execution_time_avl[0], execution_time_trad[0]])

        OP = 'Inserção'
        print(f'Executando {OP}, {i}, {sparcity}')

        benchmark_hash = """
A_hash.insert(0, 0, 1)
        """

        benchmark_avl = """
A_avl[0, 0] = 1
        """

        benchmark_trad = """
trad_A[0][0] = 1
        """

        execution_time_hash = timeit.repeat(stmt=benchmark_hash, setup=setup_code, number=10000, repeat=1)
        hash_times_i.append(execution_time_hash[0])
        
        execution_time_avl = timeit.repeat(stmt=benchmark_avl, setup=setup_code, number=10000, repeat=1)
        avl_times_i.append(execution_time_avl[0])
        
        execution_time_trad = timeit.repeat(stmt=benchmark_trad, setup=setup_code, number=10000, repeat=1) if i < 4 else [0]
        trad_times_i.append(execution_time_trad[0])

        dados.append([OP, i, sparcity, execution_time_hash[0], execution_time_avl[0], execution_time_trad[0]])

        OP = 'Multiplicação'

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
        trad_C[i][j] = 0
        for k in range(0, cols):
            trad_C[i][j] += trad_A[i][k] * trad_B[k][j]
        """

        print(f'Executando {OP}, {i}, {sparcity}')
        execution_time_hash = timeit.repeat(stmt=benchmark_hash, setup=setup_code, number=10000, repeat=1)
        hash_times_m.append(execution_time_hash[0])
        
        print(f'Executando {OP}, {i}, {sparcity}')
        execution_time_avl = timeit.repeat(stmt=benchmark_avl, setup=setup_code, number=10000, repeat=1)
        avl_times_m.append(execution_time_avl[0])
        
        print(f'Executando {OP}, {i}, {sparcity}')
        execution_time_trad = timeit.repeat(stmt=benchmark_trad, setup=setup_code, number=10000, repeat=1) if i < 0 else [0]
        trad_times_m.append(execution_time_trad[0])

        dados.append([OP, i, sparcity, execution_time_hash[0], execution_time_avl[0], execution_time_trad[0]])

        OP = "Escalar"
        print(f'Executando {OP}, {i}, {sparcity}')

        benchmark_hash = """
A_hash.times_scalar(5)
        """

        benchmark_avl = """
A_avl * 5
        """

        benchmark_trad = """
scalar = 5
for i in range(rows):
    for j in range(cols):
        trad_A[i][j] *= scalar
        """

        execution_time_hash = timeit.repeat(stmt=benchmark_hash, setup=setup_code, number=10000, repeat=1)
        hash_times_e.append(execution_time_hash[0])
        
        execution_time_avl = timeit.repeat(stmt=benchmark_avl, setup=setup_code, number=10000, repeat=1)
        avl_times_e.append(execution_time_avl[0])
        
        execution_time_trad = timeit.repeat(stmt=benchmark_trad, setup=setup_code, number=10000, repeat=1) if i < 4 else [0]
        trad_times_e.append(execution_time_trad[0])

        dados.append([OP, i, sparcity, execution_time_hash[0], execution_time_avl[0], execution_time_trad[0]])

        OP = "Transposta"
        print(f'Executando {OP}, {i}, {sparcity}')
        
        benchmark_hash = """
A_hash.transpose()
        """

        benchmark_avl = """
A_avl.transpose()
        """

        benchmark_trad = """
trad_C = []
for c in range(cols):
    trad_C.append(([0.0] * rows))
for i in range(rows):
    for j in range(cols):
        trad_C[j][i] = trad_A[i][j]
        """

        execution_time_hash = timeit.repeat(stmt=benchmark_hash, setup=setup_code, number=10000, repeat=1)
        hash_times_t.append(execution_time_hash[0])
        
        execution_time_avl = timeit.repeat(stmt=benchmark_avl, setup=setup_code, number=10000, repeat=1)
        avl_times_t.append(execution_time_avl[0])
        
        execution_time_trad = timeit.repeat(stmt=benchmark_trad, setup=setup_code, number=10000, repeat=1) if i < 4 else [0]
        trad_times_t.append(execution_time_trad[0])

        dados.append([OP, i, sparcity, execution_time_hash[0], execution_time_avl[0], execution_time_trad[0]])

    plt.figure(figsize=(8,5))
    plt.plot(sparcities, hash_times_a, marker='o', label='Hash')
    plt.plot(sparcities, avl_times_a, marker='s', label='AVL')
    plt.plot(sparcities, avl_times_a, marker='.', label='Trad')
    plt.xlabel('Sparsity')
    plt.ylabel('Execution Time (s)')
    plt.title(f"Execução de Acesso (i={i})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'Acesso_i_{i}.png')

    plt.figure(figsize=(8,5))
    plt.plot(sparcities, hash_times_s, marker='o', label='Hash')
    plt.plot(sparcities, avl_times_s, marker='s', label='AVL')
    plt.plot(sparcities, avl_times_s, marker='.', label='Trad')
    plt.xlabel('Sparsity')
    plt.ylabel('Execution Time (s)')
    plt.title(f"Execução de Soma (i={i})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'Soma_i_{i}.png')

    plt.figure(figsize=(8,5))
    plt.plot(sparcities, hash_times_i, marker='o', label='Hash')
    plt.plot(sparcities, avl_times_i, marker='s', label='AVL')
    plt.plot(sparcities, avl_times_i, marker='.', label='Trad')
    plt.xlabel('Sparsity')
    plt.ylabel('Execution Time (s)')
    plt.title(f"Execução de Inserção (i={i})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'Inserção_i_{i}.png')

    plt.figure(figsize=(8,5))
    plt.plot(sparcities, hash_times_m, marker='o', label='Hash')
    plt.plot(sparcities, avl_times_m, marker='s', label='AVL')
    plt.plot(sparcities, avl_times_m, marker='.', label='Trad')
    plt.xlabel('Sparsity')
    plt.ylabel('Execution Time (s)')
    plt.title(f"Execução de Multiplicação (i={i})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'Multiplicação_i_{i}.png')

    plt.figure(figsize=(8,5))
    plt.plot(sparcities, hash_times_e, marker='o', label='Hash')
    plt.plot(sparcities, avl_times_e, marker='s', label='AVL')
    plt.plot(sparcities, avl_times_e, marker='.', label='Trad')
    plt.xlabel('Sparsity')
    plt.ylabel('Execution Time (s)')
    plt.title(f"Execução de Escalar (i={i})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'Escalar_i_{i}.png')

    plt.figure(figsize=(8,5))
    plt.plot(sparcities, hash_times_e, marker='o', label='Hash')
    plt.plot(sparcities, avl_times_e, marker='s', label='AVL')
    plt.plot(sparcities, avl_times_e, marker='.', label='Trad')
    plt.xlabel('Sparsity')
    plt.ylabel('Execution Time (s)')
    plt.title(f"Execução de Transposta (i={i})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'Transposta_i_{i}.png')


with open(f'Tempos.csv', mode='w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    writer.writerow(['operation', 'i', 'sparsity', 'hash_time', 'avl_time', 'trad_time'])
    writer.writerows(dados)