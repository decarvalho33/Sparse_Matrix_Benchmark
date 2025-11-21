import matplotlib.pyplot as plt
import timeit
import csv
import statistics

from create_sparse_matrix_traditional import create_sparse_matrix_traditional
from algorithm_1_hash import Sparse_matrix_hash, create_sparse_matrix_hash
from algorithm_2_AVL import Sparse_matrix_AVL, create_sparse_matrix_AVL

dados = []


def medir_tempo(stmt, globals_for_timeit, i):
    """Mede o tempo conforme a regra:
       - i < 5: number=1, repeat=10, retorna mediana
       - i >= 5: number=1, repeat=1, retorna único valor
    """
    if i < 5:
        tempos = timeit.repeat(stmt=stmt,
                               globals=globals_for_timeit,
                               number=1,
                               repeat=10)
        return statistics.median(tempos)
    else:
        tempos = timeit.repeat(stmt=stmt,
                               globals=globals_for_timeit,
                               number=1,
                               repeat=1)
        return tempos[0]


for i in range(5, 7):
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
        # cria as matrizes somente UMA vez por (i, sparsidade)
        if i < 4:
            trad_A = create_sparse_matrix_traditional(i, sparcity)
            trad_B = create_sparse_matrix_traditional(i, sparcity)
            A_avl = Sparse_matrix_AVL(trad_A)
            B_avl = Sparse_matrix_AVL(trad_B)
            A_hash = Sparse_matrix_hash(trad_A)
            B_hash = Sparse_matrix_hash(trad_B)
        else:
            A_avl = create_sparse_matrix_AVL(i, sparcity)
            B_avl = create_sparse_matrix_AVL(i, sparcity)
            A_hash = create_sparse_matrix_hash(i, sparcity)
            B_hash = create_sparse_matrix_hash(i, sparcity)
            # dummies só pra não quebrar o código tradicional (que está comentado)
            trad_A = [[1.0]]
            trad_B = [[1.0]]

        rows = cols = 10**i

        # globals usados pelo timeit
        globals_for_timeit = {
            "A_hash": A_hash,
            "B_hash": B_hash,
            "A_avl": A_avl,
            "B_avl": B_avl,
            "trad_A": trad_A,
            "trad_B": trad_B,
            "rows": rows,
            "cols": cols,
        }

        # ==================== ACESSO ====================

        OP = "Acesso"
        print(f'Executando {OP}, i={i}, sparsity={sparcity}')

        benchmark_hash = "A_hash.acess(0, 0)"
        benchmark_avl  = "A_avl[0, 0]"
        benchmark_trad = "trad_A[0][0]"

        hash_time = medir_tempo(benchmark_hash, globals_for_timeit, i)
        avl_time = medir_tempo(benchmark_avl, globals_for_timeit, i)
        # trad_time = medir_tempo(benchmark_trad, globals_for_timeit, i)  # se quiser medir trad

        hash_times_a.append(hash_time)
        avl_times_a.append(avl_time)
        # trad_times_a.append(trad_time)

        dados.append([OP, i, sparcity, hash_time, avl_time])

        # ==================== SOMA ====================

        OP = "Soma"
        print(f'Executando {OP}, i={i}, sparsity={sparcity}')

        benchmark_hash = "C_hash = A_hash.plus_matrix(B_hash)"
        benchmark_avl  = "C_avl = A_avl + B_avl"
        benchmark_trad = """
trad_C = []
for c in range(cols):
    trad_C.append(([0.0] * rows))
for i_aux in range(rows):
    for j_aux in range(cols):
        trad_C[i_aux][j_aux] = trad_A[i_aux][j_aux] + trad_B[i_aux][j_aux]
        """

        hash_time = medir_tempo(benchmark_hash, globals_for_timeit, i)
        avl_time = medir_tempo(benchmark_avl, globals_for_timeit, i)
        # trad_time = medir_tempo(benchmark_trad, globals_for_timeit, i)

        hash_times_s.append(hash_time)
        avl_times_s.append(avl_time)
        # trad_times_s.append(trad_time)

        dados.append([OP, i, sparcity, hash_time, avl_time])

        # ==================== INSERÇÃO ====================

        OP = "Inserção"
        print(f'Executando {OP}, i={i}, sparsity={sparcity}')

        benchmark_hash = "A_hash.insert(0, 0, 1)"
        benchmark_avl  = "A_avl.__setitem__((0, 0), 1)"
        benchmark_trad = "trad_A[0][0] = 1"

        hash_time = medir_tempo(benchmark_hash, globals_for_timeit, i)
        avl_time = medir_tempo(benchmark_avl, globals_for_timeit, i)
        # trad_time = medir_tempo(benchmark_trad, globals_for_timeit, i)

        hash_times_i.append(hash_time)
        avl_times_i.append(avl_time)
        # trad_times_i.append(trad_time)

        dados.append([OP, i, sparcity, hash_time, avl_time])

        # ==================== MULTIPLICAÇÃO ====================

        OP = "Multiplicação"
        print(f'Executando {OP}, i={i}, sparsity={sparcity}')

        benchmark_hash = "C_hash = A_hash.times_matrix(B_hash)"
        benchmark_avl  = "C_avl = A_avl * B_avl"
        benchmark_trad = """
trad_C = []
for c in range(cols):
    trad_C.append(([0.0] * rows))
for i_aux in range(rows):
    for j_aux in range(cols):
        trad_C[i_aux][j_aux] = 0.0
        for k_aux in range(cols):
            trad_C[i_aux][j_aux] += trad_A[i_aux][k_aux] * trad_B[k_aux][j_aux]
        """

        hash_time = medir_tempo(benchmark_hash, globals_for_timeit, i)
        avl_time = medir_tempo(benchmark_avl, globals_for_timeit, i)
        # trad_time = medir_tempo(benchmark_trad, globals_for_timeit, i)

        hash_times_m.append(hash_time)
        avl_times_m.append(avl_time)
        # trad_times_m.append(trad_time)

        dados.append([OP, i, sparcity, hash_time, avl_time])

        # ==================== ESCALAR ====================

        OP = "Escalar"
        print(f'Executando {OP}, i={i}, sparsity={sparcity}')

        benchmark_hash = "A_hash.times_scalar(5)"
        benchmark_avl  = "A_avl * 5"
        benchmark_trad = """
scalar = 5
for i_aux in range(rows):
    for j_aux in range(cols):
        trad_A[i_aux][j_aux] *= scalar
        """

        hash_time = medir_tempo(benchmark_hash, globals_for_timeit, i)
        avl_time = medir_tempo(benchmark_avl, globals_for_timeit, i)
        # trad_time = medir_tempo(benchmark_trad, globals_for_timeit, i)

        hash_times_e.append(hash_time)
        avl_times_e.append(avl_time)
        # trad_times_e.append(trad_time)

        dados.append([OP, i, sparcity, hash_time, avl_time])

        # ==================== TRANSPOSTA ====================

        OP = "Transposta"
        print(f'Executando {OP}, i={i}, sparsity={sparcity}')
        
        benchmark_hash = "A_hash.transpose()"
        benchmark_avl  = "A_avl.transpose()"
        benchmark_trad = """
trad_C = []
for c in range(cols):
    trad_C.append(([0.0] * rows))
for i_aux in range(rows):
    for j_aux in range(cols):
        trad_C[j_aux][i_aux] = trad_A[i_aux][j_aux]
        """

        hash_time = medir_tempo(benchmark_hash, globals_for_timeit, i)
        avl_time = medir_tempo(benchmark_avl, globals_for_timeit, i)
        # trad_time = medir_tempo(benchmark_trad, globals_for_timeit, i)

        hash_times_t.append(hash_time)
        avl_times_t.append(avl_time)
        # trad_times_t.append(trad_time)

        dados.append([OP, i, sparcity, hash_time, avl_time])

    # ==================== GRÁFICOS POR i ====================

    plt.figure(figsize=(8,5))
    plt.plot(sparcities, hash_times_a, marker='o', label='Hash')
    plt.plot(sparcities, avl_times_a, marker='s', label='AVL')
    # plt.plot(sparcities, trad_times_a, marker='.', label='Trad')
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
    # plt.plot(sparcities, trad_times_s, marker='.', label='Trad')
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
    # plt.plot(sparcities, trad_times_i, marker='.', label='Trad')
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
    # plt.plot(sparcities, trad_times_m, marker='.', label='Trad')
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
    # plt.plot(sparcities, trad_times_e, marker='.', label='Trad')
    plt.xlabel('Sparsity')
    plt.ylabel('Execution Time (s)')
    plt.title(f"Execução de Escalar (i={i})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'Escalar_i_{i}.png')

    plt.figure(figsize=(8,5))
    plt.plot(sparcities, hash_times_t, marker='o', label='Hash')
    plt.plot(sparcities, avl_times_t, marker='s', label='AVL')
    # plt.plot(sparcities, trad_times_t, marker='.', label='Trad')
    plt.xlabel('Sparsity')
    plt.ylabel('Execution Time (s)')
    plt.title(f"Execução de Transposta (i={i})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'Transposta_i_{i}.png')

# ==================== CSV ====================

with open('Tempos.csv', mode='w', newline='') as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    writer.writerow(['operation', 'i', 'sparsity', 'hash_time', 'avl_time'])
    writer.writerows(dados)
