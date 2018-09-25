from graph import Graph
from string import ascii_lowercase
import queue


class NFAToNFDConverter:
    def __init__(self, graph):
        self.graph = graph  # Is the NFA received graph
        self.new_graph = Graph()  # Will be the NFD graph

        for node in self.graph.nodes:
            node.adjs = []

        for edge in self.graph.edges:
            node_1 = self.graph.get_node(edge.id_1)
            node_2 = self.graph.get_node(edge.id_2)
            node_1.add_adj(node_2, edge.label)

    def is_node_id_in_new_graph(self, node_id):
        is_in_graph = False
        for node in self.new_graph.nodes:
            if str(node.id) == str(node_id):
                is_in_graph = True
                break
        return is_in_graph

    def insert_nodes_to_new_graph(self, estados):
        if not estados:
            return None
        node_str = self.convert_estado_to_string(estados)
        if not self.is_node_id_in_new_graph(node_str):
            self.new_graph.create_node_with_id(node_str)
        new_node = self.new_graph.get_node(node_str)

        return new_node

    def add_node_to_new_graph(self, estados, total_edges):
        new_node = self.insert_nodes_to_new_graph(estados)

        for i in range(len(ascii_lowercase)):
            new_adj = self.insert_nodes_to_new_graph(total_edges[i])
            label = chr(i+ord('a'))

            if new_adj is not None:
                new_node.add_adj(new_adj, label)
                self.new_graph.add_edge(new_node.id, new_adj.id, label)

    def convert_estado_to_string(self, estado):
        estado_str = ""
        for node in estado:
            estado_str += str(node)
        return estado_str

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

            for i in range(len(total_edges)):
                total_edges[i] = sorted(total_edges[i])
            print(total_edges)
            print("")

            self.add_node_to_new_graph(current_nodes, total_edges)

            # Putting next element on the queue
            for i in range(len(ascii_lowercase)):
                if not total_edges[i]:  # If it is empty
                    continue

                estado = total_edges[i]
                estado_str = self.convert_estado_to_string(estado)

                is_already_in_graph = False
                for node in self.new_graph.nodes:
                    if str(node.id) == str(estado_str):
                        is_already_in_graph = True
                        break

                if not is_already_in_graph:
                    next_to_go.put(estado)

        self.new_graph.print_edges()
        self.new_graph.create_output()
