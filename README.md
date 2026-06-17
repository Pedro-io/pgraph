# pgraph

Biblioteca de criação, manipulação e análise de grafos, desenvolvida como trabalho prático da disciplina de Teoria de Grafos e Computabilidade — PUC Minas 2026/1.

## Estrutura do repositório

```
pgraph/
│
├── graph/                          # Biblioteca
│   ├── __init__.py
│   ├── abstract_graph.py
│   ├── adjacency_matrix_graph.py
│   └── adjacency_list_graph.py
│
├── notebooks/
│   ├── demo.ipynb                  # Demonstração da Etapa 1
│   └── etapa2.ipynb                # Problema real — Etapa 2
│
├── data/                          # Datasets utilizados na Etapa 2
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Como instalar e executar

### Opção 1 — Jupyter Notebook local

**Pré-requisitos:** Python 3.8+ instalado.

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/pgraph.git
cd pgraph

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Instale a biblioteca em modo desenvolvimento
pip install -e .

# 5. Abra os notebooks
jupyter notebook notebooks/
```

---

### Opção 2 — Google Colab

Abra qualquer notebook e execute a célula abaixo no início:

```python
# Instala a biblioteca direto do GitHub
!pip install git+https://github.com/seu-usuario/pgraph.git
```

Depois é só importar normalmente:

```python
from graph import AdjacencyMatrixGraph, AdjacencyListGraph
```

---

## Uso básico

```python
from graph import AdjacencyMatrixGraph, AdjacencyListGraph

# Criando um grafo com matriz de adjacência (4 vértices)
g = AdjacencyMatrixGraph(4)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.set_edge_weight(0, 1, 3.5)

print(g.has_edge(0, 1))       # True
print(g.get_edge_weight(0, 1)) # 3.5
print(g.is_connected())        # True/False

# Exportando para o Gephi
g.export_to_gephi("graph.gexf")
```

---
