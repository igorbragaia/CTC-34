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
        self.graph.edges = [edge for edge in self.graph.edges if edge.label != '&']
        initial_edges = list(self.graph.edges)

        for node in self.graph.nodes:
            node_id = node.id
            arriving_edges = [edge for edge in initial_edges if edge.id_2 == node_id]
            for next_node in self.closures[node_id]:
                for arriving_edge in arriving_edges:
                    if not self.graph.check_edge_existence(arriving_edge.id_1, next_node, arriving_edge.label):
                        self.graph.add_edge(arriving_edge.id_1, next_node, arriving_edge.label)

            leaving_edges = [edge for edge in initial_edges if edge.id_1 == node_id]
            for previous_node, closure in self.closures.items():
                if node_id in closure:
                    for leaving_edge in leaving_edges:
                        if not self.graph.check_edge_existence(previous_node, leaving_edge.id_2, leaving_edge.label):
                            self.graph.add_edge(previous_node, leaving_edge.id_2, leaving_edge.label)

        for node1, closure in self.closures.items():
            if len([node for node in closure if self.graph.nodes[node].shape == "doublecircle"]) > 0:
                self.graph.nodes[node1].shape = "doublecircle"


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

    def check_edge_existence(self, id_1, id_2, edge_name):
        for edge in self.edges:
            if edge.id_1 == id_1 and edge.id_2 == id_2 and edge.label == edge_name:
                return True
        return False

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