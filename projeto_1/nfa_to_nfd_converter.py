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
            label = edge.label

            if len(label) > 1:
                strs = label.split(',')
                for str in strs:
                    self.graph.add_edge(edge.id_1, edge.id_2, str)
                edge.label = strs[0]

        self.remove_duplicate_edges_of_new_graph(self.graph)

        for edge in self.graph.edges:
            node_1 = self.graph.get_node(edge.id_1)
            node_2 = self.graph.get_node(edge.id_2)
            node_1.add_adj(node_2, edge.label)

        graph.print_edges()

    def remove_duplicate_edges_of_new_graph(self, graph):
        length = len(graph.edges)
        i = 0

        while i < len(graph.edges):
            j = i + 1
            while j < len(graph.edges):
                if graph.edges[i].id_1 == graph.edges[j].id_1 and graph.edges[i].id_2 == \
                        graph.edges[j].id_2 and str(graph.edges[i].label) == str(graph.edges[j].label):
                    length -= 1
                    del graph.edges[j]
                else:
                    j += 1
            i += 1

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

    def add_estados_to_new_graph(self, estados, total_edges):
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

    def convert_string_to_estados(self, str):
        estados = []
        for c in str:
            estados.append(self.graph.get_node(c))

        return estados

    def nfa_to_nfd(self):
        next_to_go = queue.Queue()
        next_to_go.put([self.graph.nodes[0]])
        estados_gone = set()

        while not next_to_go.empty():
            current_nodes = next_to_go.get()
            total_edges = [[] for _ in range(len(ascii_lowercase))]

            estados_gone.add(self.convert_estado_to_string([estado.id for estado in current_nodes]))

            for current_node in current_nodes:
                alpha = ['a', 'b', 'c']
                # for character in ascii_lowercase:
                for character in alpha:
                    int_equivalent = ord(character)-ord('a')

                    for adj in current_node.adjs:
                        if adj.edge == character:
                            if adj.id not in total_edges[int_equivalent]:
                                total_edges[int_equivalent].append(adj.id)

            for i in range(len(total_edges)):
                total_edges[i] = sorted(total_edges[i])

            print("currents_node = ", [node.id for node in current_nodes])
            print("total_edges = ", total_edges)

            self.add_estados_to_new_graph([aux_node.id for aux_node in current_nodes], total_edges)

            # Putting next element on the queue
            for i in range(len(ascii_lowercase)):
                if not total_edges[i]:  # If it is empty
                    continue

                estado = total_edges[i]
                novo_estado_str = self.convert_estado_to_string(estado)

                is_already_in_graph = False
                for estados_str in estados_gone:
                    if str(estados_str) == str(novo_estado_str):
                        is_already_in_graph = True
                        break
                if not is_already_in_graph:
                    next_to_go.put([self.graph.get_node(est) for est in estado])

        new_ids = [node.id for node in self.new_graph.nodes]
        print(new_ids)

        for id in new_ids:
            is_end = False
            for node in self.convert_string_to_estados(id):
                if node.is_end_node:
                    is_end = True
                    break
            if is_end:
                self.new_graph.get_node(id).is_end_node = True
                self.new_graph.get_node(id).shape = 'doublecircle'

        self.remove_duplicate_edges_of_new_graph(self.new_graph)
        return self.new_graph
