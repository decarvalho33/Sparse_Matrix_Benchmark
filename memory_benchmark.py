import os
import psutil
import random
import matplotlib.pyplot as plt
import multiprocessing
import gc

from create_sparse_matrix_traditional import create_sparse_matrix_traditional
from algorithm_1_hash import Sparse_matrix_hash, create_sparse_matrix_hash
from algorithm_2_AVL import Sparse_matrix_AVL, create_sparse_matrix_AVL

def measure_memory(target_func, *args, **kwargs):
    """Executa uma função em um subprocesso e retorna a diferença de memória."""
    def wrapper(result_queue):
        import psutil
        import os
        import gc
        gc.collect()
        before = psutil.Process(os.getpid()).memory_info().rss
        result = target_func(*args, **kwargs)
        gc.collect()
        after = psutil.Process(os.getpid()).memory_info().rss
        result_queue.put(after - before)
    result_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=wrapper, args=(result_queue,))
    p.start()
    p.join()
    mem = result_queue.get()
    return mem / (1024 * 1024)

def sparsities_for_i(i):
    if i >= 4:
        return [1 / 10 ** (i + 2), 1 / 10 ** (i + 1), 1 / 10 ** i]
    else:
        return [0.01, 0.05, 0.1, 0.2]

# Código principal
for i in range(2, 7):
    if i >= 4:
        sparsities = sparsities_for_i(i)
    else:
        sparsities = sparsities_for_i(i)
    
    trads = []
    avls = []
    hashs = []

    for sparsity in sparsities:
        print(f"Executando para i={i} e sparsity={sparsity}...")

        if i < 4:
            def build_trad():
                return create_sparse_matrix_traditional(i, sparsity)
            mem_trad = measure_memory(build_trad)
            trads.append(mem_trad)

            def build_avl():
                A_trad = create_sparse_matrix_traditional(i, sparsity)
                return Sparse_matrix_AVL(A_trad)
            mem_avl = measure_memory(build_avl)
            avls.append(mem_avl)

            def build_hash():
                A_trad = create_sparse_matrix_traditional(i, sparsity)
                return Sparse_matrix_hash(matrix_traditional=A_trad)
            mem_hash = measure_memory(build_hash)
            hashs.append(mem_hash)

        else:
            def build_avl():
                return create_sparse_matrix_AVL(i, sparsity)
            mem_avl = measure_memory(build_avl)
            avls.append(mem_avl)

            def build_hash():
                return create_sparse_matrix_hash(i, sparsity)
            mem_hash = measure_memory(build_hash)
            hashs.append(mem_hash)
    
    plt.figure(figsize=(8,5))
    plt.plot(sparsities, hashs, marker='o', label='Hash')
    plt.plot(sparsities, avls, marker='s', label='AVL')
    if i < 4:
        plt.plot(sparsities, trads, marker='.', label='Trad')
    plt.xlabel('Sparsity')
    plt.ylabel('Memory Usage (MB)')
    plt.title(f"Execução de Transposta (i={i})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'Memory_Usage_{i}.png')
    plt.close()

print("Concluído com sucesso!")
