from graphviz import Digraph
from edge import Edge
from node import Node


class EpsilonNFAToNFA:
    def __init__(self, graph):
        self.graph = graph
        self.closures = {}

        self.create_closures(0)

        self.create_graph()

    def create_closures(self, node):
        self.closures[node] = [node]
        neighbors = [edge for edge in self.graph.edges if edge.id_1 == node]
        for edge in neighbors:
            if edge.id_2 not in self.closures:
                self.create_closures(edge.id_2)
            if edge.label == '&':
                self.closures[node].extend(self.closures[edge.id_2])

    def create_graph(self):
        edges = [edge for edge in self.graph.edges if edge.label != '&']
        self.graph.edges = []

        for node1, closure in self.closures.items():
            if len([node for node in closure if self.graph.nodes[node].shape == "doublecircle"]) > 0:
                self.graph.nodes[node1].shape = "doublecircle"

            for node2 in closure:
                neighbors = [edge for edge in edges if edge.id_1 == node2]
                for node3 in neighbors:
                    nested_closure = self.closures[node3.id_2]
                    for node4 in nested_closure:

                        self.graph.add_edge(node1, node4, node3.label)


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

    def compact_edges(self):
        length = len(self.edges)
        i = 0
        while i < len(self.edges):
            j = i+1
            while j < len(self.edges):
                if self.edges[i].id_1 == self.edges[j].id_1 and self.edges[i].id_2 == self.edges[j].id_2:
                    self.edges[i].label += "," + self.edges[j].label
                    length -= 1
                    del self.edges[j]
                else:
                    j += 1
            i += 1

    def create_output(self):
        self.compact_edges()
        for node in self.nodes:
            self.dot.node(str(node.id), shape=node.shape)
        for edge in self.edges:
            self.dot.edge(str(edge.id_1), str(edge.id_2), label=str(edge.label))

        self.dot.render('test-output/graph.gv', view=True)

    def print_nodes(self):
        for i in range(len(self.nodes)):
            print(self.nodes[i].id)

    def print_edges(self):
        print("Edges:")
        for i in range(len(self.edges)):
            print(self.edges[i].id_1, " ", self.edges[i].id_2, ": ", self.edges[i].label)
        print("")