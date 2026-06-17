"""Algoritmos de busca em profundidade (DFS) para representações de grafo."""


def dfs_list(
    adj_list: list[dict[int, float]],
    start: int,
    visited: list[bool],
    transpose: bool = False,
) -> None:
    """Percorre o grafo em profundidade a partir de *start*, marcando vértices visitados.

    Args:
        adj_list: Lista de adjacências do grafo.
        start: Vértice inicial da busca.
        visited: Lista de booleanos atualizada in-place; True indica vértice visitado.
        transpose: Se True, percorre o grafo transposto (inverte o sentido das arestas).
    """
    n = len(adj_list)
    stack = [start]
    visited[start] = True
    while stack:
        u = stack.pop()
        if transpose:
            for v in range(n):
                if not visited[v] and u in adj_list[v]:
                    visited[v] = True
                    stack.append(v)
        else:
            for v in adj_list[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)


def dfs_matrix(
    adj_matrix: list[list[float | None]],
    start: int,
    visited: list[bool],
    transpose: bool = False,
) -> None:
    """Percorre o grafo em profundidade a partir de *start*, marcando vértices visitados.

    Args:
        adj_matrix: Matriz de adjacências do grafo.
        start: Vértice inicial da busca.
        visited: Lista de booleanos atualizada in-place; True indica vértice visitado.
        transpose: Se True, percorre o grafo transposto (inverte o sentido das arestas).
    """
    n = len(adj_matrix)
    stack = [start]
    visited[start] = True
    while stack:
        u = stack.pop()
        for v in range(n):
            if not visited[v]:
                has_edge = (
                    adj_matrix[v][u] is not None
                    if transpose
                    else adj_matrix[u][v] is not None
                )
                if has_edge:
                    visited[v] = True
                    stack.append(v)
