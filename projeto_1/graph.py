from graphviz import Digraph
from edge import Edge
from node import Node

class Graph:
    def __init__(self):
        self.nodes = []
        self.dot = Digraph()
        self.edges = []
        pass

    def create_node(self, shape='circle'):
        id = len(self.nodes)
        self.nodes.append(Node(id, shape=shape))
        return id

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

    def print_nodes(self):
        for i in range(len(self.nodes)):
            print(self.nodes[i].id)

    def print_edges(self):
        for i in range(len(self.edges)):
            print(self.edges[i].id_1, " ", self.edges[i].id_2, ": ", self.edges[i].label)
