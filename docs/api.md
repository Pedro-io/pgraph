# Referência da API

Este documento descreve a API pública da biblioteca `pgraph`. A biblioteca oferece duas implementações concretas de grafo simples direcionado: `AdjacencyMatrixGraph` e `AdjacencyListGraph`. Ambas implementam a mesma interface definida por `AbstractGraph`.

## Sumário

- [Restrições do modelo de dados](#restrições-do-modelo-de-dados)
- [Instalação](#instalação)
- [Importação](#importação)
- [AdjacencyMatrixGraph](#adjacencymatrixgraph)
- [AdjacencyListGraph](#adjacencylistgraph)
- [Métodos herdados de AbstractGraph](#métodos-herdados-de-abstractgraph)
- [Exportação para Gephi](#exportação-para-gephi)
- [Exceções](#exceções)
- [Tabela de complexidades](#tabela-de-complexidades)
- [Exemplos](#exemplos)

---

## Restrições do modelo de dados

Toda implementação concreta obedece às seguintes restrições:

- **Grafo simples:** laços `(u, u)` não são permitidos e não há arestas múltiplas entre o mesmo par de vértices.
- **Grafo direcionado:** cada aresta `(u, v)` tem origem `u` e destino `v` distintos. A aresta `(v, u)` é independente de `(u, v)`.
- **Índices inteiros:** vértices são identificados por índices inteiros no intervalo `[0, num_vertices)`.
- **Pesos float:** arestas e vértices possuem peso do tipo `float`, com valor padrão `0.0`.
- **Idempotência:** `add_edge(u, v)` chamado mais de uma vez não cria arestas duplicadas nem altera o peso existente.
- **Silêncio em remoção:** `remove_edge(u, v)` não lança exceção se a aresta não existir.
- **Conectividade forte:** `is_connected()` verifica conectividade forte (todos os vértices são mutuamente alcançáveis no grafo direcionado).

---

## Instalação

**Requisitos:** Python 3.8 ou superior.

```bash
git clone https://github.com/seu-usuario/pgraph.git
cd pgraph
pip install -r requirements.txt
pip install -e .
```

Para uso no Google Colab:

```python
!pip install git+https://github.com/seu-usuario/pgraph.git
```

---

## Importação

```python
from graph import AdjacencyMatrixGraph, AdjacencyListGraph
```

---

## AdjacencyMatrixGraph

```
graph.adjacency_matrix_graph.AdjacencyMatrixGraph(num_vertices)
```

Representação por matriz de adjacências. Cada célula `_adj_matrix[u][v]` armazena o peso da aresta `(u, v)` como `float`, ou `None` quando a aresta não existe.

**Complexidade de espaço:** O(n^2), onde `n` é o número de vértices. Recomendada para grafos densos.

### Construtor

```python
AdjacencyMatrixGraph(num_vertices: int) -> None
```

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `num_vertices` | `int` | Número de vértices. Vértices são indexados de `0` a `num_vertices - 1`. |

**Exemplo:**

```python
g = AdjacencyMatrixGraph(5)  # grafo com vértices 0, 1, 2, 3, 4
```

### Métodos de aresta

#### `add_edge`

```python
add_edge(u: int, v: int) -> None
```

Adiciona a aresta `(u, v)` com peso `0.0`. Se a aresta já existir, nenhuma ação é tomada e o peso original é preservado.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `u` | `int` | Vértice de origem. |
| `v` | `int` | Vértice de destino. |

Lança `ValueError` se `u` ou `v` forem inválidos, ou se `u == v`.

Complexidade: O(1).

#### `remove_edge`

```python
remove_edge(u: int, v: int) -> None
```

Remove a aresta `(u, v)`. Se a aresta não existir, a operação é silenciosa.

Lança `ValueError` se `u` ou `v` forem inválidos.

Complexidade: O(1).

#### `has_edge`

```python
has_edge(u: int, v: int) -> bool
```

Retorna `True` se a aresta `(u, v)` existir, `False` caso contrário.

Lança `ValueError` se `u` ou `v` forem inválidos.

Complexidade: O(1).

#### `get_edge_count`

```python
get_edge_count() -> int
```

Retorna o número total de arestas no grafo. Percorre a matriz inteira.

Complexidade: O(n^2).

#### `set_edge_weight`

```python
set_edge_weight(u: int, v: int, w: float) -> None
```

Define o peso da aresta `(u, v)`.

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `u` | `int` | Vértice de origem. |
| `v` | `int` | Vértice de destino. |
| `w` | `float` | Peso a atribuir. |

Lança `ValueError` se a aresta não existir ou se os índices forem inválidos.

Complexidade: O(1).

#### `get_edge_weight`

```python
get_edge_weight(u: int, v: int) -> float
```

Retorna o peso da aresta `(u, v)`.

Lança `ValueError` se a aresta não existir ou se os índices forem inválidos.

Complexidade: O(1).

### Métodos de relacionamento

#### `is_successor`

```python
is_successor(u: int, v: int) -> bool
```

Retorna `True` se `v` for sucessor de `u`, ou seja, se existe a aresta `(u, v)`. Equivalente a `has_edge(u, v)`.

#### `is_predecessor`

```python
is_predecessor(u: int, v: int) -> bool
```

Retorna `True` se `u` for predecessor de `v`, ou seja, se existe a aresta `(u, v)`. Equivalente a `has_edge(v, u)`.

#### `is_incident`

```python
is_incident(u: int, v: int, x: int) -> bool
```

Retorna `True` se o vértice `x` for incidente à aresta `(u, v)`, ou seja, se `x == u` ou `x == v`. A aresta deve existir; caso contrário, lança `ValueError`.

### Métodos de grau

#### `get_vertex_in_degree`

```python
get_vertex_in_degree(u: int) -> int
```

Retorna o grau de entrada do vértice `u`: número de arestas `(*, u)` que chegam a `u`.

Lança `ValueError` se `u` for inválido.

Complexidade: O(n) -- percorre a coluna `u` da matriz.

#### `get_vertex_out_degree`

```python
get_vertex_out_degree(u: int) -> int
```

Retorna o grau de saída do vértice `u`: número de arestas `(u, *)` que partem de `u`.

Lança `ValueError` se `u` for inválido.

Complexidade: O(n) -- percorre a linha `u` da matriz.

### Métodos de propriedade do grafo

#### `is_connected`

```python
is_connected() -> bool
```

Verifica se o grafo é fortemente conectado. Executa duas buscas DFS iterativas a partir do vértice `0`: uma no grafo original e outra no grafo transposto. Retorna `True` se ambas visitarem todos os vértices.

Retorna `True` para grafos com zero vértices (condição vacuamente verdadeira).

Complexidade: O(n^2).

#### `is_empty_graph`

```python
is_empty_graph() -> bool
```

Retorna `True` se o grafo não possuir nenhuma aresta.

Complexidade: O(n^2).

#### `is_complete_graph`

```python
is_complete_graph() -> bool
```

Retorna `True` se o grafo possuir todas as `n * (n - 1)` arestas possíveis para um grafo simples direcionado sem laços com `n` vértices.

Complexidade: O(n^2), dominada por `get_edge_count`.

---

## AdjacencyListGraph

```
graph.adjacency_list_graph.AdjacencyListGraph(num_vertices)
```

Representação por lista de adjacências. Cada entrada `_adj_list[u]` é um dicionário `{v: peso}` que mapeia os sucessores de `u` ao peso da aresta correspondente.

**Complexidade de espaço:** O(n + m), onde `n` é o número de vértices e `m` o número de arestas. Recomendada para grafos esparsos.

### Construtor

```python
AdjacencyListGraph(num_vertices: int) -> None
```

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `num_vertices` | `int` | Número de vértices. Vértices são indexados de `0` a `num_vertices - 1`. |

**Exemplo:**

```python
g = AdjacencyListGraph(5)  # grafo com vértices 0, 1, 2, 3, 4
```

### Métodos de aresta

#### `add_edge`

```python
add_edge(u: int, v: int) -> None
```

Adiciona a aresta `(u, v)` com peso `0.0`. Se a aresta já existir, nenhuma ação é tomada e o peso original é preservado.

Lança `ValueError` se `u` ou `v` forem inválidos, ou se `u == v`.

Complexidade: O(1) amortizado.

#### `remove_edge`

```python
remove_edge(u: int, v: int) -> None
```

Remove a aresta `(u, v)`. Se a aresta não existir, a operação é silenciosa.

Lança `ValueError` se `u` ou `v` forem inválidos.

Complexidade: O(1) amortizado.

#### `has_edge`

```python
has_edge(u: int, v: int) -> bool
```

Retorna `True` se a aresta `(u, v)` existir.

Lança `ValueError` se `u` ou `v` forem inválidos.

Complexidade: O(1) amortizado (lookup em dicionário).

#### `get_edge_count`

```python
get_edge_count() -> int
```

Retorna o número total de arestas no grafo. Soma o tamanho de cada dicionário de adjacências.

Complexidade: O(n).

#### `set_edge_weight`

```python
set_edge_weight(u: int, v: int, w: float) -> None
```

Define o peso da aresta `(u, v)`.

Lança `ValueError` se a aresta não existir ou se os índices forem inválidos.

Complexidade: O(1) amortizado.

#### `get_edge_weight`

```python
get_edge_weight(u: int, v: int) -> float
```

Retorna o peso da aresta `(u, v)`.

Lança `ValueError` se a aresta não existir ou se os índices forem inválidos.

Complexidade: O(1) amortizado.

### Métodos de relacionamento

#### `is_successor`

```python
is_successor(u: int, v: int) -> bool
```

Retorna `True` se `v` for sucessor de `u`. Equivalente a `has_edge(u, v)`.

#### `is_predecessor`

```python
is_predecessor(u: int, v: int) -> bool
```

Retorna `True` se `u` for predecessor de `v`. Equivalente a `has_edge(v, u)`.

#### `is_incident`

```python
is_incident(u: int, v: int, x: int) -> bool
```

Retorna `True` se `x == u` ou `x == v`. A aresta deve existir; caso contrário, lança `ValueError`.

### Métodos de grau

#### `get_vertex_in_degree`

```python
get_vertex_in_degree(u: int) -> int
```

Retorna o grau de entrada do vértice `u`.

Lança `ValueError` se `u` for inválido.

Complexidade: O(n + m) -- percorre todas as listas de adjacências para contar quantas contêm `u`.

#### `get_vertex_out_degree`

```python
get_vertex_out_degree(u: int) -> int
```

Retorna o grau de saída do vértice `u`.

Lança `ValueError` se `u` for inválido.

Complexidade: O(1) -- tamanho do dicionário `_adj_list[u]`.

### Métodos de propriedade do grafo

#### `is_connected`

```python
is_connected() -> bool
```

Verifica se o grafo é fortemente conectado. Executa duas buscas DFS iterativas a partir do vértice `0`: uma no grafo original e outra no grafo transposto.

Complexidade: O(n + m).

#### `is_empty_graph`

```python
is_empty_graph() -> bool
```

Retorna `True` se nenhum dicionário de adjacências possuir entradas.

Complexidade: O(n).

#### `is_complete_graph`

```python
is_complete_graph() -> bool
```

Retorna `True` se o grafo possuir todas as `n * (n - 1)` arestas possíveis.

Complexidade: O(n).

---

## Métodos herdados de AbstractGraph

Ambas as classes herdam os métodos a seguir diretamente de `AbstractGraph`, sem override.

### `get_vertex_count`

```python
get_vertex_count() -> int
```

Retorna o número de vértices do grafo.

### `set_vertex_weight`

```python
set_vertex_weight(v: int, w: float) -> None
```

Define o peso do vértice `v`. Peso padrão é `0.0`.

Lança `ValueError` se `v` for inválido.

### `get_vertex_weight`

```python
get_vertex_weight(v: int) -> float
```

Retorna o peso do vértice `v`.

Lança `ValueError` se `v` for inválido.

### `is_divergent`

```python
is_divergent(u1: int, v1: int, u2: int, v2: int) -> bool
```

Retorna `True` se as arestas `(u1, v1)` e `(u2, v2)` forem divergentes, ou seja, se compartilham a mesma origem (`u1 == u2`).

Lança `ValueError` se qualquer índice for inválido.

### `is_convergent`

```python
is_convergent(u1: int, v1: int, u2: int, v2: int) -> bool
```

Retorna `True` se as arestas `(u1, v1)` e `(u2, v2)` forem convergentes, ou seja, se compartilham o mesmo destino (`v1 == v2`).

Lança `ValueError` se qualquer índice for inválido.

---

## Exportação para Gephi

```python
export_to_gephi(path: str) -> None
```

Exporta o grafo para um arquivo compatível com o Gephi. O formato de saída é determinado pela extensão do arquivo informado em `path`.

| Extensão | Formato |
|----------|---------|
| `.gexf` | GEXF 1.3 (Graph Exchange XML Format) |
| `.graphml` | GraphML (XML) |
| `.csv` | Lista de arestas com colunas `source`, `target`, `weight` |

Lança `ValueError` se a extensão não for suportada.
Lança `OSError` se não for possível escrever no caminho especificado.

**Exemplos:**

```python
g.export_to_gephi("saida.gexf")
g.export_to_gephi("saida.graphml")
g.export_to_gephi("saida.csv")
```

O arquivo GEXF inclui pesos de vértices como atributo `weight` em cada nó. O arquivo GraphML registra pesos de vértices (`vweight`) e de arestas (`eweight`) como chaves separadas. O arquivo CSV não exporta pesos de vértices.

---

## Exceções

| Exceção | Quando ocorre |
|---------|---------------|
| `ValueError` | Índice de vértice fora do intervalo `[0, num_vertices)` |
| `ValueError` | Tentativa de adicionar laço `(u, u)` |
| `ValueError` | `set_edge_weight` ou `get_edge_weight` em aresta inexistente |
| `ValueError` | `is_incident` em aresta inexistente |
| `ValueError` | Extensão de arquivo inválida em `export_to_gephi` |
| `OSError` | Falha de escrita em `export_to_gephi` |

---

## Tabela de complexidades

A tabela compara as complexidades de tempo das operações entre as duas implementações. `n` é o número de vértices e `m` o número de arestas.

| Operação | AdjacencyMatrixGraph | AdjacencyListGraph |
|----------|---------------------|--------------------|
| `add_edge` | O(1) | O(1) amortizado |
| `remove_edge` | O(1) | O(1) amortizado |
| `has_edge` | O(1) | O(1) amortizado |
| `get_edge_count` | O(n^2) | O(n) |
| `set_edge_weight` | O(1) | O(1) amortizado |
| `get_edge_weight` | O(1) | O(1) amortizado |
| `get_vertex_in_degree` | O(n) | O(n + m) |
| `get_vertex_out_degree` | O(n) | O(1) |
| `is_connected` | O(n^2) | O(n + m) |
| `is_empty_graph` | O(n^2) | O(n) |
| `is_complete_graph` | O(n^2) | O(n) |
| Espaço | O(n^2) | O(n + m) |

**Quando usar cada representação:**

- `AdjacencyMatrixGraph`: grafos densos (m próximo de n^2), quando `has_edge` é a operação dominante, ou quando a memória não é restrição.
- `AdjacencyListGraph`: grafos esparsos (m muito menor que n^2), quando grau de saída ou iteração sobre sucessores é frequente.

---

## Exemplos

### Grafo básico com pesos

```python
from graph import AdjacencyMatrixGraph

g = AdjacencyMatrixGraph(4)

g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 0)

g.set_edge_weight(0, 1, 1.5)
g.set_edge_weight(1, 2, 2.0)
g.set_edge_weight(2, 3, 0.5)
g.set_edge_weight(3, 0, 3.0)

print(g.has_edge(0, 1))           # True
print(g.get_edge_weight(0, 1))    # 1.5
print(g.get_edge_count())         # 4
print(g.is_connected())           # True
print(g.is_complete_graph())      # False
```

### Pesos de vértices

```python
from graph import AdjacencyListGraph

g = AdjacencyListGraph(3)

g.set_vertex_weight(0, 10.0)
g.set_vertex_weight(1, 20.0)
g.set_vertex_weight(2, 30.0)

print(g.get_vertex_weight(0))     # 10.0
print(g.get_vertex_count())       # 3
```

### Graus de entrada e saída

```python
from graph import AdjacencyListGraph

g = AdjacencyListGraph(4)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(3, 1)

print(g.get_vertex_out_degree(0)) # 2
print(g.get_vertex_in_degree(1))  # 2  (arestas (0,1) e (3,1))
print(g.get_vertex_in_degree(0))  # 0
```

### Relações entre arestas

```python
from graph import AdjacencyMatrixGraph

g = AdjacencyMatrixGraph(4)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)

# Divergentes: mesma origem
print(g.is_divergent(0, 1, 0, 2))  # True   -- ambas partem de 0
print(g.is_divergent(0, 1, 1, 3))  # False  -- origens distintas

# Convergentes: mesmo destino
print(g.is_convergent(0, 1, 0, 1)) # True   -- mesmo destino 1
print(g.is_convergent(0, 1, 0, 2)) # False  -- destinos distintos

# Incidência
print(g.is_incident(0, 1, 0))      # True   -- 0 é a origem
print(g.is_incident(0, 1, 1))      # True   -- 1 é o destino
print(g.is_incident(0, 1, 2))      # False
```

### Verificação de sucessor e predecessor

```python
from graph import AdjacencyMatrixGraph

g = AdjacencyMatrixGraph(3)
g.add_edge(0, 1)

print(g.is_successor(0, 1))    # True  -- existe aresta (0, 1)
print(g.is_successor(1, 0))    # False -- não existe aresta (1, 0)

print(g.is_predecessor(0, 1))  # True  -- 0 precede 1
print(g.is_predecessor(1, 0))  # False -- 1 não precede 0
```

### Exportação

```python
from graph import AdjacencyMatrixGraph

g = AdjacencyMatrixGraph(3)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.set_edge_weight(0, 1, 5.0)
g.set_vertex_weight(0, 1.0)

g.export_to_gephi("grafo.gexf")    # GEXF com pesos de nós e arestas
g.export_to_gephi("grafo.graphml") # GraphML com atributos separados
g.export_to_gephi("grafo.csv")     # CSV: source,target,weight
```

### Grafo vazio e completo

```python
from graph import AdjacencyListGraph

g = AdjacencyListGraph(3)
print(g.is_empty_graph())     # True

g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 0)
g.add_edge(1, 2)
g.add_edge(2, 0)
g.add_edge(2, 1)

print(g.is_complete_graph())  # True  -- 3*(3-1) = 6 arestas
print(g.is_empty_graph())     # False
```
