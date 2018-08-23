from node import Node
from graphviz import Digraph


class Graph:
    def __init__(self):
        self.nodes = []
        self.dot = Digraph()
        pass

    def add_node(self, node):
        self.nodes.append(node)
        self.dot.node(str(node.id))

    def add_edge(self, id_1, id_2):
        self.dot.edge(str(id_1), str(id_2))

    def create_output(self):
        self.dot.render('test-output/graph.gv', view=True)

    def print_graph(self):
        print(self.dot)
