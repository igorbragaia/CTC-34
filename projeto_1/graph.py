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

    def epsilon_nfa_to_nfa(self):
        self.__create_closures(0)
        self.__rewrite_graph()

    def strings_accepted(self, chain):
        ids_possible_states = [0]
        ids_possible_states_aux = []
        for i in range(len(chain)):
            for current_id_possible_state in ids_possible_states:
                for j in range(len(self.edges)):
                    if (self.edges[j].id_1 == current_id_possible_state) and (chain[i] in self.edges[j].label):
                        ids_possible_states_aux.append(self.edges[j].id_2)
            ids_possible_states = []
            for j in ids_possible_states_aux:
                ids_possible_states.append(j)
            ids_possible_states_aux = []
        for i in ids_possible_states:
            if self.nodes[i].shape == 'doublecircle':
                return True
        return False

    def substrings_accepted(self, chain):
        print("Sub-cadeias aceitas:")
        accepted_strings = []
        for i in range(len(chain) + 1):
            for j in range(len(chain) + 1):
                if j >= i:
                    subchain = chain[i:j]
                    accepted = self.strings_accepted(subchain)
                    if accepted and subchain not in accepted_strings:
                        accepted_strings.append(subchain)
        for subchain in accepted_strings:
            print(subchain)

    def __create_closures(self, node):
        self.closures[node] = [node]
        neighbors = [edge for edge in self.edges if edge.id_1 == node]
        for edge in neighbors:
            if edge.id_2 not in self.closures:
                self.__create_closures(edge.id_2)
            if edge.label == '&':
                self.closures[node].extend(self.closures[edge.id_2])

    def __rewrite_graph(self):
        edges = list(self.edges)

        for edge in edges:
            if edge.label == '&':
                self.remove_edge(edge.id_1, edge.id_2, edge.label)

        initial_edges = list(self.edges)

        for node in self.nodes:
            node_id = node.id
            arriving_edges = [edge for edge in initial_edges if edge.id_2 == node_id]
            for next_node in self.closures[node_id]:
                for arriving_edge in arriving_edges:
                    if not self.check_edge_existence(arriving_edge.id_1, next_node, arriving_edge.label):
                        self.add_edge(arriving_edge.id_1, next_node, arriving_edge.label)

            leaving_edges = [edge for edge in initial_edges if edge.id_1 == node_id]
            for previous_node, closure in self.closures.items():
                if node_id in closure:
                    for leaving_edge in leaving_edges:
                        if not self.check_edge_existence(previous_node, leaving_edge.id_2, leaving_edge.label):
                            self.add_edge(previous_node, leaving_edge.id_2, leaving_edge.label)

        for node1, closure in self.closures.items():
            if len([node for node in closure if self.nodes[node].shape == "doublecircle"]) > 0:
                self.nodes[node1].shape = "doublecircle"

