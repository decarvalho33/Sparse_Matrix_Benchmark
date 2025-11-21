class Sparse_matrix_hash:
    """
    Implementação de matriz esparsa usando tabela hash com encadeamento separado.
    Cada bucket guarda entradas [ib, jb, val] em coordenadas internas.
    Coordenadas lógicas (i, j) levam em conta transposição.
    """

    def __init__(self, matrix_traditional=None, n_rows=None, n_cols=None, capacity=100000):
        # define dimensões
        if matrix_traditional is not None:
            n_rows = len(matrix_traditional)
            n_cols = len(matrix_traditional[0]) if n_rows > 0 else 0
        if n_rows is None or n_cols is None:
            raise ValueError("É preciso informar matrix_traditional ou (n_rows, n_cols).")

        self.n_rows = n_rows            # dimensões lógicas atuais
        self.n_cols = n_cols
        self.base_n_cols = n_cols       # usado na função de hash (colunas da orientação base)
        self.capacity = max(1, capacity)
        self.size = 0                   # nº de elementos não nulos
        self.is_transposed = False      # se True, interface lógica está transposta
        self.buckets = [[] for _ in range(self.capacity)]

        # carrega matriz tradicional (se fornecida)
        if matrix_traditional is not None:
            for i in range(n_rows):
                row = matrix_traditional[i]
                for j in range(n_cols):
                    val = row[j]
                    if val != 0:
                        self._insert_internal(i, j, val, check_resize=True)

    # ====================== interface pública ======================

    def acess(self, i, j):
        """Retorna A[i, j] na visão lógica (considerando transposição)."""
        ib, jb = self._logical_to_internal(i, j)
        bucket_index, pos = self.find_entry(ib, jb)
        if pos is None:
            return 0.0
        return self.buckets[bucket_index][pos][2]

    def insert(self, i, j, x):
        """Define A[i, j] = x na visão lógica. Se x == 0, remove o elemento."""
        ib, jb = self._logical_to_internal(i, j)
        bucket_index, pos = self.find_entry(ib, jb)
        bucket = self.buckets[bucket_index]

        if x == 0.0:
            if pos is not None:
                bucket.pop(pos)
                self.size -= 1
            return

        if pos is None:
            # chave nova
            bucket.append([ib, jb, x])
            self.size += 1
        else:
            # atualiza
            bucket[pos][2] = x

        self.maybe_resize()

    def transpose(self):
        """Transpõe a matriz de forma preguiçosa (só troca flags/dimensões)."""
        self.is_transposed = not self.is_transposed
        self.n_rows, self.n_cols = self.n_cols, self.n_rows
        # base_n_cols continua sendo o número de colunas da orientação base
        return self

    def plus_matrix(self, B):
        """Retorna C = self + B."""
        if self.n_rows != B.n_rows or self.n_cols != B.n_cols:
            raise ValueError("Dimensões incompatíveis para soma.")
        if self.is_transposed != B.is_transposed:
            raise ValueError("As duas matrizes devem estar no mesmo estado de transposição.")

        P = Sparse_matrix_hash(n_rows=self.n_rows,
                               n_cols=self.n_cols,
                               capacity=max(self.capacity, B.capacity))
        # mesma orientação/base
        P.is_transposed = self.is_transposed
        P.base_n_cols = self.base_n_cols

        for i, j, val in self.items():
            P.insert(i, j, val)

        for i, j, val in B.items():
            atual = P.acess(i, j)
            P.insert(i, j, atual + val)

        return P

    def times_scalar(self, a):
        """Retorna S = a * self."""
        S = Sparse_matrix_hash(n_rows=self.n_rows,
                               n_cols=self.n_cols,
                               capacity=self.capacity)
        S.is_transposed = self.is_transposed
        S.base_n_cols = self.base_n_cols

        for i, j, val in self.items():
            S.insert(i, j, a * val)

        return S

    def times_matrix(self, B):
        """Retorna C = self * B."""
        if self.n_cols != B.n_rows:
            raise ValueError("Dimensões incompatíveis para multiplicação.")
        if self.is_transposed != B.is_transposed:
            raise ValueError("As duas matrizes devem estar no mesmo estado de transposição.")

        C = Sparse_matrix_hash(n_rows=self.n_rows,
                               n_cols=B.n_cols,
                               capacity=max(self.capacity, B.capacity))

        # versão simples: produto via todos os pares não nulos
        A_items = list(self.items())
        B_items = list(B.items())

        for i, j, a_val in A_items:
            for j2, k, b_val in B_items:
                if j2 == j:
                    atual = C.acess(i, k)
                    C.insert(i, k, atual + a_val * b_val)

        return C

    # ====================== auxiliares públicas ======================

    def getSize(self):
        return self.size

    def getBuckets(self):
        return self.buckets

    # ====================== funções internas ======================

    def _logical_to_internal(self, i, j):
        """Converte coordenadas lógicas (i, j) para internas (ib, jb)."""
        if self.is_transposed:
            return j, i
        return i, j

    def hash(self, ib, jb):
        """Função de hash nas coordenadas internas."""
        return (ib * self.base_n_cols + jb) % self.capacity

    def find_entry(self, ib, jb):
        bucket_index = self.hash(ib, jb)
        bucket = self.buckets[bucket_index]

        for pos, (i2, j2, _) in enumerate(bucket):
            if i2 == ib and j2 == jb:
                return bucket_index, pos
        return bucket_index, None

    def maybe_resize(self):
        """Redimensiona a tabela se o fator de carga ultrapassar 0.75."""
        if self.capacity == 0:
            return
        load_factor = self.size / self.capacity
        if load_factor > 0.75:
            self.resize()

    def resize(self):
        """Dobra a capacidade e faz re-hash de todos os elementos."""
        old_buckets = self.buckets
        old_capacity = self.capacity

        self.capacity = max(1, 2 * old_capacity)
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0  # será recalculado

        for bucket in old_buckets:
            for ib, jb, val in bucket:
                self._insert_internal(ib, jb, val, check_resize=False)

    def _insert_internal(self, ib, jb, x, check_resize):
        """Insere usando coordenadas internas; usado em __init__ e resize."""
        bucket_index = self.hash(ib, jb)
        bucket = self.buckets[bucket_index]

        for pos, (i2, j2, _) in enumerate(bucket):
            if i2 == ib and j2 == jb:
                bucket[pos][2] = x
                break
        else:
            bucket.append([ib, jb, x])
            self.size += 1

        if check_resize:
            self.maybe_resize()

    def items(self):
        """Itera sobre (i, j, val) em coordenadas lógicas."""
        for bucket in self.buckets:
            for ib, jb, val in bucket:
                if self.is_transposed:
                    yield jb, ib, val
                else:
                    yield ib, jb, val
