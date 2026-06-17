# Referencia da API

Este documento descreve a API publica da biblioteca `pgraph`. A biblioteca oferece duas implementacoes concretas de grafo simples direcionado: `AdjacencyMatrixGraph` e `AdjacencyListGraph`. Ambas implementam a mesma interface definida por `AbstractGraph`.

## Sumario

- [Restricoes do modelo de dados](#restricoes-do-modelo-de-dados)
- [Instalacao](#instalacao)
- [Importacao](#importacao)
- [AdjacencyMatrixGraph](#adjacencymatrixgraph)
- [AdjacencyListGraph](#adjacencylistgraph)
- [Metodos herdados de AbstractGraph](#metodos-herdados-de-abstractgraph)
- [Exportacao para Gephi](#exportacao-para-gephi)
- [Excecoes](#excecoes)
- [Tabela de complexidades](#tabela-de-complexidades)
- [Exemplos](#exemplos)

---

## Restricoes do modelo de dados

Toda implementacao concreta obedece as seguintes restricoes:

- **Grafo simples:** lacos `(u, u)` nao sao permitidos e nao ha arestas multiplas entre o mesmo par de vertices.
- **Grafo direcionado:** cada aresta `(u, v)` tem origem `u` e destino `v` distintos. A aresta `(v, u)` e independente de `(u, v)`.
- **Indices inteiros:** vertices sao identificados por indices inteiros no intervalo `[0, num_vertices)`.
- **Pesos float:** arestas e vertices possuem peso do tipo `float`, com valor padrao `0.0`.
- **Idempotencia:** `add_edge(u, v)` chamado mais de uma vez nao cria arestas duplicadas nem altera o peso existente.
- **Silencio em remocao:** `remove_edge(u, v)` nao lanca excecao se a aresta nao existir.
- **Conectividade forte:** `is_connected()` verifica conectividade forte (todos os vertices sao mutuamente alcancaveis no grafo direcionado).

---

## Instalacao

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

## Importacao

```python
from graph import AdjacencyMatrixGraph, AdjacencyListGraph
```

---

## AdjacencyMatrixGraph

```
graph.adjacency_matrix_graph.AdjacencyMatrixGraph(num_vertices)
```

Representacao por matriz de adjacencias. Cada celula `_adj_matrix[u][v]` armazena o peso da aresta `(u, v)` como `float`, ou `None` quando a aresta nao existe.

**Complexidade de espaco:** O(n^2), onde `n` e o numero de vertices. Recomendada para grafos densos.

### Construtor

```python
AdjacencyMatrixGraph(num_vertices: int) -> None
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `num_vertices` | `int` | Numero de vertices. Vertices sao indexados de `0` a `num_vertices - 1`. |

**Exemplo:**

```python
g = AdjacencyMatrixGraph(5)  # grafo com vertices 0, 1, 2, 3, 4
```

### Metodos de aresta

#### `add_edge`

```python
add_edge(u: int, v: int) -> None
```

Adiciona a aresta `(u, v)` com peso `0.0`. Se a aresta ja existir, nenhuma acao e tomada e o peso original e preservado.

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `u` | `int` | Vertice de origem. |
| `v` | `int` | Vertice de destino. |

Lanca `ValueError` se `u` ou `v` forem invalidos, ou se `u == v`.

Complexidade: O(1).

#### `remove_edge`

```python
remove_edge(u: int, v: int) -> None
```

Remove a aresta `(u, v)`. Se a aresta nao existir, a operacao e silenciosa.

Lanca `ValueError` se `u` ou `v` forem invalidos.

Complexidade: O(1).

#### `has_edge`

```python
has_edge(u: int, v: int) -> bool
```

Retorna `True` se a aresta `(u, v)` existir, `False` caso contrario.

Lanca `ValueError` se `u` ou `v` forem invalidos.

Complexidade: O(1).

#### `get_edge_count`

```python
get_edge_count() -> int
```

Retorna o numero total de arestas no grafo. Percorre a matriz inteira.

Complexidade: O(n^2).

#### `set_edge_weight`

```python
set_edge_weight(u: int, v: int, w: float) -> None
```

Define o peso da aresta `(u, v)`.

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `u` | `int` | Vertice de origem. |
| `v` | `int` | Vertice de destino. |
| `w` | `float` | Peso a atribuir. |

Lanca `ValueError` se a aresta nao existir ou se os indices forem invalidos.

Complexidade: O(1).

#### `get_edge_weight`

```python
get_edge_weight(u: int, v: int) -> float
```

Retorna o peso da aresta `(u, v)`.

Lanca `ValueError` se a aresta nao existir ou se os indices forem invalidos.

Complexidade: O(1).

### Metodos de relacionamento

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

Retorna `True` se o vertice `x` for incidente a aresta `(u, v)`, ou seja, se `x == u` ou `x == v`. A aresta deve existir; caso contrario, lanca `ValueError`.

### Metodos de grau

#### `get_vertex_in_degree`

```python
get_vertex_in_degree(u: int) -> int
```

Retorna o grau de entrada do vertice `u`: numero de arestas `(*, u)` que chegam a `u`.

Lanca `ValueError` se `u` for invalido.

Complexidade: O(n) -- percorre a coluna `u` da matriz.

#### `get_vertex_out_degree`

```python
get_vertex_out_degree(u: int) -> int
```

Retorna o grau de saida do vertice `u`: numero de arestas `(u, *)` que partem de `u`.

Lanca `ValueError` se `u` for invalido.

Complexidade: O(n) -- percorre a linha `u` da matriz.

### Metodos de propriedade do grafo

#### `is_connected`

```python
is_connected() -> bool
```

Verifica se o grafo e fortemente conectado. Executa duas buscas DFS iterativas a partir do vertice `0`: uma no grafo original e outra no grafo transposto. Retorna `True` se ambas visitarem todos os vertices.

Retorna `True` para grafos com zero vertices (condicao vacuamente verdadeira).

Complexidade: O(n^2).

#### `is_empty_graph`

```python
is_empty_graph() -> bool
```

Retorna `True` se o grafo nao possuir nenhuma aresta.

Complexidade: O(n^2).

#### `is_complete_graph`

```python
is_complete_graph() -> bool
```

Retorna `True` se o grafo possuir todas as `n * (n - 1)` arestas possiveis para um grafo simples direcionado sem lacos com `n` vertices.

Complexidade: O(n^2), dominada por `get_edge_count`.

---

## AdjacencyListGraph

```
graph.adjacency_list_graph.AdjacencyListGraph(num_vertices)
```

Representacao por lista de adjacencias. Cada entrada `_adj_list[u]` e um dicionario `{v: peso}` que mapeia os sucessores de `u` ao peso da aresta correspondente.

**Complexidade de espaco:** O(n + m), onde `n` e o numero de vertices e `m` o numero de arestas. Recomendada para grafos esparsos.

### Construtor

```python
AdjacencyListGraph(num_vertices: int) -> None
```

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `num_vertices` | `int` | Numero de vertices. Vertices sao indexados de `0` a `num_vertices - 1`. |

**Exemplo:**

```python
g = AdjacencyListGraph(5)  # grafo com vertices 0, 1, 2, 3, 4
```

### Metodos de aresta

#### `add_edge`

```python
add_edge(u: int, v: int) -> None
```

Adiciona a aresta `(u, v)` com peso `0.0`. Se a aresta ja existir, nenhuma acao e tomada e o peso original e preservado.

Lanca `ValueError` se `u` ou `v` forem invalidos, ou se `u == v`.

Complexidade: O(1) amortizado.

#### `remove_edge`

```python
remove_edge(u: int, v: int) -> None
```

Remove a aresta `(u, v)`. Se a aresta nao existir, a operacao e silenciosa.

Lanca `ValueError` se `u` ou `v` forem invalidos.

Complexidade: O(1) amortizado.

#### `has_edge`

```python
has_edge(u: int, v: int) -> bool
```

Retorna `True` se a aresta `(u, v)` existir.

Lanca `ValueError` se `u` ou `v` forem invalidos.

Complexidade: O(1) amortizado (lookup em dicionario).

#### `get_edge_count`

```python
get_edge_count() -> int
```

Retorna o numero total de arestas no grafo. Soma o tamanho de cada dicionario de adjacencias.

Complexidade: O(n).

#### `set_edge_weight`

```python
set_edge_weight(u: int, v: int, w: float) -> None
```

Define o peso da aresta `(u, v)`.

Lanca `ValueError` se a aresta nao existir ou se os indices forem invalidos.

Complexidade: O(1) amortizado.

#### `get_edge_weight`

```python
get_edge_weight(u: int, v: int) -> float
```

Retorna o peso da aresta `(u, v)`.

Lanca `ValueError` se a aresta nao existir ou se os indices forem invalidos.

Complexidade: O(1) amortizado.

### Metodos de relacionamento

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

Retorna `True` se `x == u` ou `x == v`. A aresta deve existir; caso contrario, lanca `ValueError`.

### Metodos de grau

#### `get_vertex_in_degree`

```python
get_vertex_in_degree(u: int) -> int
```

Retorna o grau de entrada do vertice `u`.

Lanca `ValueError` se `u` for invalido.

Complexidade: O(n + m) -- percorre todas as listas de adjacencias para contar quantas contem `u`.

#### `get_vertex_out_degree`

```python
get_vertex_out_degree(u: int) -> int
```

Retorna o grau de saida do vertice `u`.

Lanca `ValueError` se `u` for invalido.

Complexidade: O(1) -- tamanho do dicionario `_adj_list[u]`.

### Metodos de propriedade do grafo

#### `is_connected`

```python
is_connected() -> bool
```

Verifica se o grafo e fortemente conectado. Executa duas buscas DFS iterativas a partir do vertice `0`: uma no grafo original e outra no grafo transposto.

Complexidade: O(n + m).

#### `is_empty_graph`

```python
is_empty_graph() -> bool
```

Retorna `True` se nenhum dicionario de adjacencias possuir entradas.

Complexidade: O(n).

#### `is_complete_graph`

```python
is_complete_graph() -> bool
```

Retorna `True` se o grafo possuir todas as `n * (n - 1)` arestas possiveis.

Complexidade: O(n).

---

## Metodos herdados de AbstractGraph

Ambas as classes herdam os metodos a seguir diretamente de `AbstractGraph`, sem override.

### `get_vertex_count`

```python
get_vertex_count() -> int
```

Retorna o numero de vertices do grafo.

### `set_vertex_weight`

```python
set_vertex_weight(v: int, w: float) -> None
```

Define o peso do vertice `v`. Peso padrao e `0.0`.

Lanca `ValueError` se `v` for invalido.

### `get_vertex_weight`

```python
get_vertex_weight(v: int) -> float
```

Retorna o peso do vertice `v`.

Lanca `ValueError` se `v` for invalido.

### `is_divergent`

```python
is_divergent(u1: int, v1: int, u2: int, v2: int) -> bool
```

Retorna `True` se as arestas `(u1, v1)` e `(u2, v2)` forem divergentes, ou seja, se compartilham a mesma origem (`u1 == u2`).

Lanca `ValueError` se qualquer indice for invalido.

### `is_convergent`

```python
is_convergent(u1: int, v1: int, u2: int, v2: int) -> bool
```

Retorna `True` se as arestas `(u1, v1)` e `(u2, v2)` forem convergentes, ou seja, se compartilham o mesmo destino (`v1 == v2`).

Lanca `ValueError` se qualquer indice for invalido.

---

## Exportacao para Gephi

```python
export_to_gephi(path: str) -> None
```

Exporta o grafo para um arquivo compativel com o Gephi. O formato de saida e determinado pela extensao do arquivo informado em `path`.

| Extensao | Formato |
|----------|---------|
| `.gexf` | GEXF 1.3 (Graph Exchange XML Format) |
| `.graphml` | GraphML (XML) |
| `.csv` | Lista de arestas com colunas `source`, `target`, `weight` |

Lanca `ValueError` se a extensao nao for suportada.
Lanca `OSError` se nao for possivel escrever no caminho especificado.

**Exemplos:**

```python
g.export_to_gephi("saida.gexf")
g.export_to_gephi("saida.graphml")
g.export_to_gephi("saida.csv")
```

O arquivo GEXF inclui pesos de vertices como atributo `weight` em cada no. O arquivo GraphML registra pesos de vertices (`vweight`) e de arestas (`eweight`) como chaves separadas. O arquivo CSV nao exporta pesos de vertices.

---

## Excecoes

| Excecao | Quando ocorre |
|---------|---------------|
| `ValueError` | Indice de vertice fora do intervalo `[0, num_vertices)` |
| `ValueError` | Tentativa de adicionar laco `(u, u)` |
| `ValueError` | `set_edge_weight` ou `get_edge_weight` em aresta inexistente |
| `ValueError` | `is_incident` em aresta inexistente |
| `ValueError` | Extensao de arquivo invalida em `export_to_gephi` |
| `OSError` | Falha de escrita em `export_to_gephi` |

---

## Tabela de complexidades

A tabela compara as complexidades de tempo das operacoes entre as duas implementacoes. `n` e o numero de vertices e `m` o numero de arestas.

| Operacao | AdjacencyMatrixGraph | AdjacencyListGraph |
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
| Espaco | O(n^2) | O(n + m) |

**Quando usar cada representacao:**

- `AdjacencyMatrixGraph`: grafos densos (m proximo de n^2), quando `has_edge` e a operacao dominante, ou quando a memoria nao e restricao.
- `AdjacencyListGraph`: grafos esparsos (m muito menor que n^2), quando grau de saida ou iteracao sobre sucessores e frequente.

---

## Exemplos

### Grafo basico com pesos

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

### Pesos de vertices

```python
from graph import AdjacencyListGraph

g = AdjacencyListGraph(3)

g.set_vertex_weight(0, 10.0)
g.set_vertex_weight(1, 20.0)
g.set_vertex_weight(2, 30.0)

print(g.get_vertex_weight(0))     # 10.0
print(g.get_vertex_count())       # 3
```

### Graus de entrada e saida

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

### Relacoes entre arestas

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

# Incidencia
print(g.is_incident(0, 1, 0))      # True   -- 0 e a origem
print(g.is_incident(0, 1, 1))      # True   -- 1 e o destino
print(g.is_incident(0, 1, 2))      # False
```

### Verificacao de sucessor e predecessor

```python
from graph import AdjacencyMatrixGraph

g = AdjacencyMatrixGraph(3)
g.add_edge(0, 1)

print(g.is_successor(0, 1))    # True  -- existe aresta (0, 1)
print(g.is_successor(1, 0))    # False -- nao existe aresta (1, 0)

print(g.is_predecessor(0, 1))  # True  -- 0 precede 1
print(g.is_predecessor(1, 0))  # False -- 1 nao precede 0
```

### Exportacao

```python
from graph import AdjacencyMatrixGraph

g = AdjacencyMatrixGraph(3)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.set_edge_weight(0, 1, 5.0)
g.set_vertex_weight(0, 1.0)

g.export_to_gephi("grafo.gexf")    # GEXF com pesos de nos e arestas
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
