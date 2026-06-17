from abstract_graph import AbstractGraph
from utils.dfs import dfs_matrix


class AdjacencyMatrixGraph(AbstractGraph):
    """Grafo simples direcionado representado por matriz de adjacências.

    Cada célula ``_adj_matrix[u][v]`` armazena o peso da aresta ``(u, v)``
    como ``float``, ou ``None`` quando a aresta não existe. Laços são
    proibidos e arestas múltiplas não são suportadas.

    Complexidade de espaço: O(n²), onde *n* é o número de vértices.

    Vértices são identificados por índices inteiros no intervalo
    ``[0, num_vertices)``.

    Args:
        num_vertices: Quantidade de vértices do grafo.

    Example:
        >>> g = AdjacencyMatrixGraph(3)
        >>> g.add_edge(0, 1)
        >>> g.has_edge(0, 1)
        True
    """

    def __init__(self, num_vertices: int) -> None:
        super().__init__(num_vertices)
        self._adj_matrix: list[list[float | None]] = [
            [None] * num_vertices for _ in range(num_vertices)
        ]

    def get_edge_count(self) -> int:
        """Retorna a quantidade de arestas existentes no grafo.

        Percorre toda a matriz para contar células não nulas.

        Returns:
            Número de arestas presentes.

        Note:
            Complexidade: O(n²).
        """
        count = 0
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self._adj_matrix[i][j] is not None:
                    count += 1
        return count

    def has_edge(self, u: int, v: int) -> bool:
        """Verifica se existe uma aresta direcionada de ``u`` para ``v``.

        Args:
            u: Vértice de origem.
            v: Vértice de destino.

        Returns:
            ``True`` se a aresta ``(u, v)`` existir, ``False`` caso contrário.

        Raises:
            ValueError: Se ``u`` ou ``v`` forem índices inválidos.

        Note:
            Complexidade: O(1).
        """
        self._validate_vertex(u, v)
        return self._adj_matrix[u][v] is not None

    def add_edge(self, u: int, v: int) -> None:
        """Adiciona uma aresta direcionada de ``u`` para ``v`` com peso 0.0.

        Idempotente: se a aresta já existir, nenhuma ação é tomada e o peso
        original é preservado.

        Args:
            u: Vértice de origem.
            v: Vértice de destino.

        Raises:
            ValueError: Se ``u`` ou ``v`` forem índices inválidos, ou se
                ``u == v`` (laços não são permitidos).

        Note:
            Complexidade: O(1). Para definir um peso diferente de 0.0, use
            :meth:`set_edge_weight` após adicionar a aresta.
        """
        self._validate_vertex(u, v)
        if u == v:
            raise ValueError("Laços (u, u) não são permitidos.")

        if self._adj_matrix[u][v] is not None:
            self.logger.debug(f"Aresta ({u}, {v}) já existe. Nenhuma ação tomada.")

        if self._adj_matrix[u][v] is None:
            self._adj_matrix[u][v] = 0.0

    def remove_edge(self, u: int, v: int) -> None:
        """Remove a aresta direcionada de ``u`` para ``v``, se existir.

        Operação silenciosa: se a aresta não existir, nada acontece.

        Args:
            u: Vértice de origem.
            v: Vértice de destino.

        Raises:
            ValueError: Se ``u`` ou ``v`` forem índices inválidos.

        Note:
            Complexidade: O(1).
        """
        self._validate_vertex(u, v)
        if self._adj_matrix[u][v] is None:
            self.logger.debug(f"Aresta ({u}, {v}) não existe. Nenhuma ação tomada.")
        else:
            self._adj_matrix[u][v] = None

    def is_successor(self, u: int, v: int) -> bool:
        """Verifica se ``v`` é sucessor de ``u``, ou seja, se existe aresta ``(u, v)``.

        Args:
            u: Vértice de origem.
            v: Candidato a sucessor.

        Returns:
            ``True`` se ``v`` for sucessor de ``u``.

        Raises:
            ValueError: Se ``u`` ou ``v`` forem índices inválidos.
        """
        return self.has_edge(u, v)

    def is_predecessor(self, u: int, v: int) -> bool:
        """Verifica se ``u`` é predecessor de ``v``, ou seja, se existe aresta ``(u, v)``.

        Args:
            u: Candidato a predecessor.
            v: Vértice de destino.

        Returns:
            ``True`` se ``u`` for predecessor de ``v``.

        Raises:
            ValueError: Se ``u`` ou ``v`` forem índices inválidos.
        """
        return self.has_edge(v, u)

    def is_incident(self, u: int, v: int, x: int) -> bool:
        """Verifica se o vértice ``x`` é incidente à aresta ``(u, v)``.

        Um vértice é incidente a uma aresta se ele é um dos seus extremos,
        ou seja, ``x == u`` ou ``x == v``. A aresta deve existir no grafo.

        Args:
            u: Origem da aresta.
            v: Destino da aresta.
            x: Vértice a verificar.

        Returns:
            ``True`` se ``x == u`` ou ``x == v``.

        Raises:
            ValueError: Se algum índice for inválido ou se a aresta
                ``(u, v)`` não existir.
        """
        self._validate_vertex(u, v, x)
        if not self.has_edge(u, v):
            raise ValueError(f"Aresta ({u}, {v}) não existe.")
        return x == u or x == v

    def get_vertex_in_degree(self, u: int) -> int:
        """Retorna o grau de entrada do vértice ``u``.

        O grau de entrada é o número de arestas ``(*, u)`` que chegam a ``u``.

        Args:
            u: Vértice alvo.

        Returns:
            Número de arestas cujo destino é ``u``.

        Raises:
            ValueError: Se ``u`` for índice inválido.

        Note:
            Complexidade: O(n).
        """
        self._validate_vertex(u)
        in_degree = 0
        for v in range(self.num_vertices):
            if self._adj_matrix[v][u] is not None:
                in_degree += 1
        return in_degree

    def get_vertex_out_degree(self, u: int) -> int:
        """Retorna o grau de saída do vértice ``u``.

        O grau de saída é o número de arestas ``(u, *)`` que partem de ``u``.

        Args:
            u: Vértice alvo.

        Returns:
            Número de arestas cuja origem é ``u``.

        Raises:
            ValueError: Se ``u`` for índice inválido.

        Note:
            Complexidade: O(n).
        """
        self._validate_vertex(u)
        out_degree = 0
        for v in range(self.num_vertices):
            if self._adj_matrix[u][v] is not None:
                out_degree += 1
        return out_degree

    def is_connected(self) -> bool:
        """Verifica se o grafo é fortemente conectado.

        Usa duas buscas em profundidade (DFS): uma no grafo original e outra
        no grafo transposto, ambas a partir do vértice 0. O grafo é
        fortemente conectado se e somente se as duas buscas visitam todos os
        vértices.

        Returns:
            ``True`` se o grafo for fortemente conectado, ``True`` também
            para grafos com zero vértices (vácuamente verdadeiro).

        Note:
            Complexidade: O(n²).
        """
        if self.num_vertices == 0:
            return True

        visited = [False] * self.num_vertices
        dfs_matrix(self._adj_matrix, 0, visited)
        if not all(visited):
            return False

        visited = [False] * self.num_vertices
        dfs_matrix(self._adj_matrix, 0, visited, transpose=True)
        return all(visited)

    def is_empty_graph(self) -> bool:
        """Verifica se o grafo não possui nenhuma aresta.

        Returns:
            ``True`` se ``get_edge_count() == 0``.

        Note:
            Complexidade: O(n²). Para verificações frequentes em grafos
            grandes, considere manter um contador de arestas.
        """
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self._adj_matrix[i][j] is not None:
                    return False
        return True

    def is_complete_graph(self) -> bool:
        """Verifica se o grafo possui todas as arestas possíveis.

        Para um grafo simples direcionado sem laços com *n* vértices, o
        número máximo de arestas é ``n * (n - 1)``.

        Returns:
            ``True`` se ``get_edge_count() == num_vertices * (num_vertices - 1)``.

        Note:
            Complexidade: O(n²), dominada por :meth:`get_edge_count`.
        """
        expected_edge_count = self.num_vertices * (self.num_vertices - 1)
        return self.get_edge_count() == expected_edge_count

    def export_to_gephi(self, path: str) -> None:
        """Exporta o grafo em formato compatível com o Gephi.

        A extensão do arquivo em *path* determina o formato de saída:
        ``.gexf``, ``.graphml`` ou ``.csv``.

        Args:
            path: Caminho do arquivo de saída (ex.: ``"grafo.gexf"``).

        Raises:
            ValueError: Se o formato inferido pela extensão não for
                suportado.
            OSError: Se não for possível escrever no caminho especificado.

        Note:
            Não implementado.
        """
        raise NotImplementedError
