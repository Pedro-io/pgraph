"""Grafo simples direcionado representado por lista de adjacências."""

from .abstract_graph import AbstractGraph
from .utils.dfs import dfs_list


class AdjacencyListGraph(AbstractGraph):
    """Grafo simples direcionado representado por lista de adjacências.

    Cada entrada ``_adj_list[u]`` é um dicionário ``{v: peso}`` que mapeia
    os sucessores de ``u`` ao peso da aresta correspondente. Laços são
    proibidos e arestas múltiplas não são suportadas.

    Complexidade de espaço: O(n + m), onde *n* é o número de vértices e
    *m* o número de arestas.

    Vértices são identificados por índices inteiros no intervalo
    ``[0, num_vertices)``.

    Args:
        num_vertices: Quantidade de vértices do grafo.

    Example:
        >>> g = AdjacencyListGraph(3)
        >>> g.add_edge(0, 1)
        >>> g.has_edge(0, 1)
        True
    """

    def __init__(self, num_vertices: int) -> None:
        super().__init__(num_vertices)
        self._adj_list: list[dict[int, float]] = [{} for _ in range(num_vertices)]

    def get_edge_count(self) -> int:
        """Retorna a quantidade de arestas existentes no grafo.

        Soma o número de entradas em cada dicionário de adjacências.

        Returns:
            Número de arestas presentes.

        Note:
            Complexidade: O(n).
        """
        return sum(len(neighbors) for neighbors in self._adj_list)

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
            Complexidade: O(1) amortizado (lookup em dicionário).
        """
        self._validate_vertex(u, v)
        return v in self._adj_list[u]

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
            Complexidade: O(1) amortizado. Para definir um peso diferente de
            0.0, use :meth:`set_edge_weight` após adicionar a aresta.
        """
        self._validate_vertex(u, v)
        if u == v:
            raise ValueError("Laços (u, u) não são permitidos.")

        if v in self._adj_list[u]:
            self.logger.debug(f"Aresta ({u}, {v}) já existe. Nenhuma ação tomada.")
        else:
            self._adj_list[u][v] = 0.0

    def remove_edge(self, u: int, v: int) -> None:
        """Remove a aresta direcionada de ``u`` para ``v``, se existir.

        Operação silenciosa: se a aresta não existir, nada acontece.

        Args:
            u: Vértice de origem.
            v: Vértice de destino.

        Raises:
            ValueError: Se ``u`` ou ``v`` forem índices inválidos.

        Note:
            Complexidade: O(1) amortizado.
        """
        self._validate_vertex(u, v)
        if v not in self._adj_list[u]:
            self.logger.debug(f"Aresta ({u}, {v}) não existe. Nenhuma ação tomada.")
        else:
            del self._adj_list[u][v]

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
            Complexidade: O(n + m), onde *m* é o número total de arestas.
        """
        self._validate_vertex(u)
        return sum(1 for neighbors in self._adj_list if u in neighbors)

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
            Complexidade: O(1).
        """
        self._validate_vertex(u)
        return len(self._adj_list[u])

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
            Complexidade: O(n + m).
        """
        if self.num_vertices == 0:
            return True

        visited = [False] * self.num_vertices
        dfs_list(self._adj_list, 0, visited)
        if not all(visited):
            return False

        visited = [False] * self.num_vertices
        dfs_list(self._adj_list, 0, visited, transpose=True)
        return all(visited)

    def is_empty_graph(self) -> bool:
        """Verifica se o grafo não possui nenhuma aresta.

        Returns:
            ``True`` se ``get_edge_count() == 0``.

        Note:
            Complexidade: O(n).
        """
        return all(len(neighbors) == 0 for neighbors in self._adj_list)

    def is_complete_graph(self) -> bool:
        """Verifica se o grafo possui todas as arestas possíveis.

        Para um grafo simples direcionado sem laços com *n* vértices, o
        número máximo de arestas é ``n * (n - 1)``.

        Returns:
            ``True`` se ``get_edge_count() == num_vertices * (num_vertices - 1)``.

        Note:
            Complexidade: O(n).
        """
        expected_edge_count = self.num_vertices * (self.num_vertices - 1)
        return self.get_edge_count() == expected_edge_count

    def set_edge_weight(self, u: int, v: int, w: float) -> None:
        """Define o peso da aresta (u, v).

        Args:
            u: Vértice de origem.
            v: Vértice de destino.
            w: Peso a atribuir.

        Raises:
            ValueError: Se u ou v forem índices inválidos ou se a aresta
                (u, v) não existir.

        Note:
            Complexidade: O(1) amortizado.
        """
        self._validate_vertex(u, v)
        if v not in self._adj_list[u]:
            raise ValueError(f"Aresta ({u}, {v}) não existe.")
        self._adj_list[u][v] = w

    def get_edge_weight(self, u: int, v: int) -> float:
        """Retorna o peso da aresta (u, v).

        Args:
            u: Vértice de origem.
            v: Vértice de destino.

        Returns:
            Peso associado à aresta (u, v).

        Raises:
            ValueError: Se u ou v forem índices inválidos ou se a aresta
                (u, v) não existir.

        Note:
            Complexidade: O(1) amortizado.
        """
        self._validate_vertex(u, v)
        if v not in self._adj_list[u]:
            raise ValueError(f"Aresta ({u}, {v}) não existe.")
        return self._adj_list[u][v]
