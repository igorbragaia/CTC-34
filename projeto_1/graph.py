from graphviz import Digraph
from edge import Edge


class Graph:
    def __init__(self):
        self.nodes = []
        self.dot = Digraph()
        self.edges = []
        pass

    def add_node(self, node):
        self.nodes.append(node)

    def get_node(self, id):
        for i in range(len(self.nodes)):
            if self.nodes[i].id == id:
                return self.nodes[i]
        print("Node with id = ", id, " not found in function get_node")

    def add_edge(self, id_1, id_2, edge_name):
        node_1 = self.get_node(id_1)
        node_2 = self.get_node(id_2)
        node_1.add_adj(node_2, edge_name)
        self.edges.append(Edge(id_1, id_2, edge_name))

    def create_output(self):
        for node in self.nodes:
            self.dot.node(str(node.id), shape=node.shape)
        for edge in self.edges:
            self.dot.edge(str(edge.id_1), str(edge.id_2), label=str(edge.label))

        self.dot.render('test-output/graph.gv', view=True)

    def print_graph(self):
        print(self.dot)

        for i in range(len(self.nodes)):
            print(self.nodes[i].id)
