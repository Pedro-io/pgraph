# pgraph

Biblioteca de criação, manipulação e análise de grafos simples direcionados, desenvolvida como trabalho prático da disciplina de Teoria de Grafos e Computabilidade na PUC Minas 2026/1.

Para a referência técnica completa de todos os métodos, parâmetros, exceções e complexidades, consulte [docs/api.md](docs/api.md).

## Estrutura do repositório

```
pgraph/
|
|-- graph/                          # Biblioteca
|   |-- __init__.py
|   |-- abstract_graph.py
|   |-- adjacency_matrix_graph.py
|   |-- adjacency_list_graph.py
|   `-- utils/
|       |-- dfs.py
|       `-- logger.py
|
|-- notebooks/                      # Exemplos de uso
|-- docs/
|   `-- api.md                      # Referência da API
|-- data/
|-- pyproject.toml
|-- requirements.txt
`-- README.md
```

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

## Uso básico

```python
from graph import AdjacencyMatrixGraph, AdjacencyListGraph

g = AdjacencyMatrixGraph(4)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.set_edge_weight(0, 1, 3.5)

print(g.has_edge(0, 1))        # True
print(g.get_edge_weight(0, 1)) # 3.5
print(g.is_connected())        # True/False

g.export_to_gephi("grafo.gexf")
```

Para exemplos mais completos, incluindo pesos de vértices, graus, relações entre arestas e exportação, consulte [docs/api.md](docs/api.md).
