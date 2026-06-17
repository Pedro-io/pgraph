def dfs_matrix(
    adj_matrix: list[list[float | None]],
    start: int,
    visited: list[bool],
    transpose: bool = False,
) -> None:
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
