from graph import Graph
from collections import deque
from string import ascii_lowercase
import queue


class Converter:
    def __init__(self, graph):
        self.graph = graph  # Is the NFA received graph
        self.new_graph = Graph()  # Will be the NFD graph

        for node in self.graph.nodes:
            node.adjs = []

        for edge in self.graph.edges:
            edge.print()
            node_1 = self.graph.get_node(edge.id_1)
            node_2 = self.graph.get_node(edge.id_2)
            node_1.add_adj(node_2, edge.label)

    def getPossivelEstado(self, proxEstado, current_node):
        pass

    def iterate_throught_the_alphabet(self, possivelEstado, node, current_node):
        pass

    def get_estados_from_string(self, estados_str):
        estados = []
        for i in range(len(estados_str)):
            c = str(estados_str)[i]
            estados.append(self.graph.get_node(c))
        return estados

    def nfa_to_nfd(self):
        next_to_go = queue.Queue()
        next_to_go.put([self.graph.nodes[0]])

        while not next_to_go.empty():
            current_nodes = next_to_go.get()
            total_edges = [[] for _ in range(len(ascii_lowercase))]

            for current_node in current_nodes:
                print("current_node.id = ", current_node.id)

                for character in ascii_lowercase:
                    int_equivalent = ord(character)-ord('a')

                    for adj in current_node.adjs:
                        if adj.edge == character:
                            print("char = " + character + ", adj.id = " + str(adj.id))
                            if adj.id not in total_edges[int_equivalent]:
                                total_edges[int_equivalent].append(adj.id)

                # for i in range(len(total_edges)):
                #     total_edges[i] = sorted(total_edges[i])

                print(total_edges)
