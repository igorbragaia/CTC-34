from graphviz import Digraph
from edge import Edge
from node import Node
import uuid


class Graph:
    def __init__(self):
        self.nodes = []
        self.dot = Digraph()
        self.edges = []
        self.compacted_edges = []
        self.closures = {}

    def create_node(self, shape='circle'):
        id = len(self.nodes)
        self.nodes.append(Node(id, shape=shape))
        return id

    def create_node_with_id(self, id, shape='circle'):
        self.nodes.append(Node(id, shape=shape))
        return id

    def get_node(self, id):
        for i in range(len(self.nodes)):
            if str(self.nodes[i].id) == str(id):
                return self.nodes[i]
        print("Node with id = ", id, " not found in function get_node")
        return None

    def add_edge(self, id_1, id_2, edge_name):
        node_1 = self.get_node(id_1)
        node_2 = self.get_node(id_2)
        node_1.add_adj(node_2, edge_name)
        self.edges.append(Edge(id_1, id_2, edge_name))

    def remove_edge(self, id_1, id_2, edge_name):
        if self.check_edge_existence(id_1, id_2, edge_name):
            self.edges = [edge for edge in self.edges if
                          not (edge.id_1 == id_1 and edge.id_2 == id_2 and edge.label == edge_name)]
            node_1 = self.get_node(id_1)
            node_1.adjs = [node for node in node_1.adjs if not node.id == id_2]
            node_2 = self.get_node(id_2)
            node_2.adjs = [node for node in node_2.adjs if not node.id == id_1]

    def remove_node(self, node_id):
        for i in range(len(self.nodes)):
            node = self.nodes[i]

            if str(node.id) == str(node_id):
                for adj in node.adjs:
                    


                del self.nodes[i]


        if self.check_edge_existence(id_1, id_2, edge_name):
            self.edges = [edge for edge in self.edges if
                          not (edge.id_1 == id_1 and edge.id_2 == id_2 and edge.label == edge_name)]
            node_1 = self.get_node(id_1)
            node_1.adjs = [node for node in node_1.adjs if not node.id == id_2]
            node_2 = self.get_node(id_2)
            node_2.adjs = [node for node in node_2.adjs if not node.id == id_1]

    def check_edge_existence(self, id_1, id_2, edge_name):
        for edge in self.edges:
            if edge.id_1 == id_1 and edge.id_2 == id_2 and edge.label == edge_name:
                return True
        return False

    def compact_edges(self):
        self.compacted_edges = list(self.edges)
        length = len(self.compacted_edges)
        i = 0
        while i < len(self.compacted_edges):
            j = i + 1
            while j < len(self.compacted_edges):
                if self.compacted_edges[i].id_1 == self.compacted_edges[j].id_1 and self.compacted_edges[i].id_2 == \
                        self.compacted_edges[j].id_2:
                    self.compacted_edges[i].label += "," + self.compacted_edges[j].label
                    length -= 1
                    del self.compacted_edges[j]
                else:
                    j += 1
            i += 1

    def create_output(self):
        self.compact_edges()
        for node in self.nodes:
            self.dot.node(str(node.id), shape=node.shape)
        for edge in self.compacted_edges:
            self.dot.edge(str(edge.id_1), str(edge.id_2), label=str(edge.label))

        self.dot.render('test-output/graph.gv', view=True, cleanup=False)

    def print_nodes(self):
        for i in range(len(self.nodes)):
            print(self.nodes[i].id)

    def print_edges(self):
        print("Edges:")
        for i in range(len(self.edges)):
            print(self.edges[i].id_1, " ", self.edges[i].id_2, ": ", self.edges[i].label)
        print("")

