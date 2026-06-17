"""Interface abstrata comum para grafos simples direcionados."""

from abc import ABC, abstractmethod

from .utils import logger as logger_module


class AbstractGraph(ABC):
    """API comum para grafos simples direcionados.

    Define a interface que todas as representações concretas devem implementar
    (matriz de adjacência, lista de adjacência, etc.). Contém atributos
    compartilhados e métodos auxiliares reutilizados pelas subclasses.

    Restrições impostas a toda implementação concreta:
    - Grafos simples: sem laços (u, u) e sem arestas múltiplas.
    - addEdge é idempotente: chamadas repetidas não criam arestas duplicadas.
    - Índices de vértices válidos: 0 ≤ v < num_vertices.
    - Exceções devem ser lançadas para índices inválidos e para operações
      inconsistentes (ex.: consultar peso de aresta inexistente).

    Args:
        num_vertices: Quantidade de vértices do grafo. Os vértices são
            identificados por índices inteiros no intervalo [0, num_vertices).
        logger: Instância de logger para registro de eventos e erros.
    """

    def __init__(self, num_vertices: int, logger=None) -> None:
        if logger is None:
            logger = logger_module.logger
        self.num_vertices = num_vertices
        self._vertex_weights: list[float] = [0.0] * num_vertices
        self.logger = logger

    def _validate_vertex(self, *vertices: int) -> None:
        """Lança ValueError se algum índice estiver fora do intervalo válido."""
        self.logger.debug(f"Validando vértices: {vertices}")
        for v in vertices:
            if v < 0 or v >= self.num_vertices:
                raise ValueError(
                    f"Índice de vértice inválido: {v}. "
                    f"Esperado no intervalo [0, {self.num_vertices})."
                )

    def get_vertex_count(self) -> int:
        """Retorna a quantidade de vértices do grafo."""
        return self.num_vertices

    @abstractmethod
    def get_edge_count(self) -> int:
        """Retorna a quantidade de arestas existentes no grafo."""

    @abstractmethod
    def has_edge(self, u: int, v: int) -> bool:
        """Verifica se existe uma aresta direcionada de u para v.

        Args:
            u: Vértice de origem.
            v: Vértice de destino.

        Returns:
            True se a aresta (u, v) existir, False caso contrário.

        Raises:
            ValueError: Se u ou v forem índices inválidos.
        """

    @abstractmethod
    def add_edge(self, u: int, v: int) -> None:
        """Adiciona uma aresta direcionada de u para v.

        Idempotente: chamadas repetidas com os mesmos vértices não criam
        arestas duplicadas. Laços (u, u) não são permitidos.

        Args:
            u: Vértice de origem.
            v: Vértice de destino.

        Raises:
            ValueError: Se u ou v forem índices inválidos, ou se u == v.
        """

    @abstractmethod
    def remove_edge(self, u: int, v: int) -> None:
        """Remove a aresta direcionada de u para v, caso exista.

        Se a aresta não existir, a operação é silenciosa (sem exceção).

        Args:
            u: Vértice de origem.
            v: Vértice de destino.

        Raises:
            ValueError: Se u ou v forem índices inválidos.
        """

    @abstractmethod
    def is_successor(self, u: int, v: int) -> bool:
        """Verifica se v é sucessor de u, ou seja, se existe aresta (u, v).

        Args:
            u: Vértice de origem.
            v: Candidato a sucessor.

        Returns:
            True se v for sucessor de u.

        Raises:
            ValueError: Se u ou v forem índices inválidos.
        """

    @abstractmethod
    def is_predecessor(self, u: int, v: int) -> bool:
        """Verifica se u é predecessor de v, ou seja, se existe aresta (u, v).

        Args:
            u: Candidato a predecessor.
            v: Vértice de destino.

        Returns:
            True se u for predecessor de v.

        Raises:
            ValueError: Se u ou v forem índices inválidos.
        """

    def is_divergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        """Verifica se as arestas (u1, v1) e (u2, v2) são divergentes.

        Duas arestas são divergentes quando possuem o mesmo vértice de origem
        (u1 == u2).

        Args:
            u1: Origem da primeira aresta.
            v1: Destino da primeira aresta.
            u2: Origem da segunda aresta.
            v2: Destino da segunda aresta.

        Returns:
            True se u1 == u2.

        Raises:
            ValueError: Se algum índice for inválido.
        """
        self._validate_vertex(u1, v1, u2, v2)
        return u1 == u2

    def is_convergent(self, u1: int, v1: int, u2: int, v2: int) -> bool:
        """Verifica se as arestas (u1, v1) e (u2, v2) são convergentes.

        Duas arestas são convergentes quando possuem o mesmo vértice de destino
        (v1 == v2).

        Args:
            u1: Origem da primeira aresta.
            v1: Destino da primeira aresta.
            u2: Origem da segunda aresta.
            v2: Destino da segunda aresta.

        Returns:
            True se v1 == v2.

        Raises:
            ValueError: Se algum índice for inválido.
        """
        self._validate_vertex(u1, v1, u2, v2)
        return v1 == v2

    @abstractmethod
    def is_incident(self, u: int, v: int, x: int) -> bool:
        """Verifica se o vértice x é incidente à aresta (u, v).

        Um vértice x é incidente a uma aresta se x == u ou x == v.

        Args:
            u: Origem da aresta.
            v: Destino da aresta.
            x: Vértice a verificar.

        Returns:
            True se x for u ou v.

        Raises:
            ValueError: Se algum índice for inválido.
        """

    @abstractmethod
    def get_vertex_in_degree(self, u: int) -> int:
        """Retorna o grau de entrada do vértice u.

        O grau de entrada é o número de arestas que chegam a u.

        Args:
            u: Vértice alvo.

        Returns:
            Número de arestas (*, u) no grafo.

        Raises:
            ValueError: Se u for índice inválido.
        """

    @abstractmethod
    def get_vertex_out_degree(self, u: int) -> int:
        """Retorna o grau de saída do vértice u.

        O grau de saída é o número de arestas que partem de u.

        Args:
            u: Vértice alvo.

        Returns:
            Número de arestas (u, *) no grafo.

        Raises:
            ValueError: Se u for índice inválido.
        """

    def set_vertex_weight(self, v: int, w: float) -> None:
        """Define o peso do vértice v.

        Args:
            v: Índice do vértice.
            w: Peso a atribuir.

        Raises:
            ValueError: Se v for índice inválido.
        """
        self._validate_vertex(v)
        self._vertex_weights[v] = w

    def get_vertex_weight(self, v: int) -> float:
        """Retorna o peso do vértice v.

        Args:
            v: Índice do vértice.

        Returns:
            Peso associado ao vértice v.

        Raises:
            ValueError: Se v for índice inválido.
        """
        self._validate_vertex(v)
        return self._vertex_weights[v]

    @abstractmethod
    def set_edge_weight(self, u: int, v: int, w: float) -> None:
        """Define o peso da aresta (u, v).

        Args:
            u: Vértice de origem.
            v: Vértice de destino.
            w: Peso a atribuir.

        Raises:
            ValueError: Se u ou v forem índices inválidos ou se a aresta
                (u, v) não existir.
        """

    @abstractmethod
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
        """

    @abstractmethod
    def is_connected(self) -> bool:
        """Verifica se o grafo é conectado.

        Considera a conectividade fraca: o grafo subjacente não direcionado
        deve ser conectado (todos os vértices alcançáveis entre si).

        Returns:
            True se o grafo for conectado.
        """

    @abstractmethod
    def is_empty_graph(self) -> bool:
        """Verifica se o grafo não possui arestas.

        Returns:
            True se get_edge_count() == 0.
        """

    @abstractmethod
    def is_complete_graph(self) -> bool:
        """Verifica se o grafo possui todas as arestas possíveis.

        Para um grafo simples direcionado sem laços com n vértices, o número
        máximo de arestas é n * (n - 1).

        Returns:
            True se get_edge_count() == num_vertices * (num_vertices - 1).
        """

    def export_to_gephi(self, path: str) -> None:
        """Exporta o grafo em formato compatível com o Gephi.

        Formatos aceitos: .gexf, .graphml ou .csv. A extensão do arquivo
        em *path* determina o formato de saída.

        Args:
            path: Caminho do arquivo de saída (ex.: "grafo.gexf").

        Raises:
            ValueError: Se o formato inferido pela extensão não for suportado.
            OSError: Se não for possível escrever no caminho especificado.
        """
        ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
        if ext == "gexf":
            self._export_gexf(path)
        elif ext == "graphml":
            self._export_graphml(path)
        elif ext == "csv":
            self._export_csv(path)
        else:
            raise ValueError(
                f"Formato não suportado: '.{ext}'. Use .gexf, .graphml ou .csv."
            )

    def _export_gexf(self, path: str) -> None:
        import xml.etree.ElementTree as ET

        gexf = ET.Element("gexf", {"xmlns": "http://gexf.net/1.3"})
        graph = ET.SubElement(gexf, "graph", defaultedgetype="directed")

        attrs = ET.SubElement(graph, "attributes", {"class": "node"})
        ET.SubElement(
            attrs, "attribute", {"id": "weight", "title": "weight", "type": "float"}
        )

        nodes_el = ET.SubElement(graph, "nodes")
        for v in range(self.num_vertices):
            node = ET.SubElement(nodes_el, "node", id=str(v), label=str(v))
            attvalues = ET.SubElement(node, "attvalues")
            ET.SubElement(
                attvalues,
                "attvalue",
                {"for": "weight", "value": str(self.get_vertex_weight(v))},
            )

        edges_el = ET.SubElement(graph, "edges")
        edge_id = 0
        for u in range(self.num_vertices):
            for v in range(self.num_vertices):
                if self.has_edge(u, v):
                    ET.SubElement(
                        edges_el,
                        "edge",
                        id=str(edge_id),
                        source=str(u),
                        target=str(v),
                        weight=str(self.get_edge_weight(u, v)),
                    )
                    edge_id += 1

        tree = ET.ElementTree(gexf)
        ET.indent(tree, space="  ")
        tree.write(path, encoding="unicode", xml_declaration=True)

    def _export_graphml(self, path: str) -> None:
        import xml.etree.ElementTree as ET

        graphml = ET.Element("graphml", {"xmlns": "http://graphml.graphdrawing.org/graphml"})
        ET.SubElement(
            graphml,
            "key",
            {"id": "vweight", "for": "node", "attr.name": "weight", "attr.type": "double"},
        )
        ET.SubElement(
            graphml,
            "key",
            {"id": "eweight", "for": "edge", "attr.name": "weight", "attr.type": "double"},
        )

        graph = ET.SubElement(graphml, "graph", id="G", edgedefault="directed")
        for v in range(self.num_vertices):
            node = ET.SubElement(graph, "node", id=f"n{v}")
            data = ET.SubElement(node, "data", key="vweight")
            data.text = str(self.get_vertex_weight(v))

        edge_id = 0
        for u in range(self.num_vertices):
            for v in range(self.num_vertices):
                if self.has_edge(u, v):
                    edge = ET.SubElement(
                        graph, "edge", id=f"e{edge_id}", source=f"n{u}", target=f"n{v}"
                    )
                    data = ET.SubElement(edge, "data", key="eweight")
                    data.text = str(self.get_edge_weight(u, v))
                    edge_id += 1

        tree = ET.ElementTree(graphml)
        ET.indent(tree, space="  ")
        tree.write(path, encoding="unicode", xml_declaration=True)

    def _export_csv(self, path: str) -> None:
        import csv

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["source", "target", "weight"])
            for u in range(self.num_vertices):
                for v in range(self.num_vertices):
                    if self.has_edge(u, v):
                        writer.writerow([u, v, self.get_edge_weight(u, v)])
