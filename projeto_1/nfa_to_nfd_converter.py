from graph import Graph
from string import ascii_lowercase
import queue


class NFAToNFDConverter:
    def __init__(self, graph):
        self.graph = graph  # Is the NFA received graph
        self.new_graph = Graph()  # Will be the NFD graph
        self.alpha = []

        for edge in graph.edges:
            if edge.label not in self.alpha:
                self.alpha.append(edge.label)

        self.alpha = sorted(self.alpha)

        self.remove_duplicate_edges_of_new_graph(self.graph)

    def remove_duplicate_edges_of_new_graph(self, graph):
        for edge in self.graph.edges:
            label = edge.label

            if len(label) > 1:
                strs = label.split(',')
                for s in strs:
                    self.graph.add_edge(edge.id_1, edge.id_2, s)
                edge.label = strs[0]

        length = len(graph.edges)
        i = 0

        while i < len(graph.edges):
            j = i + 1
            while j < len(graph.edges):
                if str(graph.edges[i].id_1) == str(graph.edges[j].id_1) and str(graph.edges[i].id_2) == \
                        str(graph.edges[j].id_2) and str(graph.edges[i].label) == str(graph.edges[j].label):
                    length -= 1
                    print("Removing")
                    del graph.edges[j]
                else:
                    j += 1
            i += 1

        for node in self.graph.nodes:
            node.adjs = []
            node.edges = []

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

    def add_estados_to_new_graph(self, estados, total_edges):
        new_node = self.insert_nodes_to_new_graph(estados)

        for i in range(len(self.alpha)):
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

    def add_null_state_for_new_graph(self):
        null_id = self.new_graph.create_node_with_id("Ø")
        for character in self.alpha:
            self.new_graph.add_edge(null_id, null_id, character)

        for node in self.new_graph.nodes:
            for character in self.alpha:
                hasEdge = False
                for edge in node.edges:
                    if str(edge) == character:
                        hasEdge = True
                        break
                if not hasEdge:
                    self.new_graph.add_edge(node.id, null_id, character)

        has_at_least_one_edge = False
        for edge in self.new_graph.edges:
            if (edge.id_1 == null_id and edge.id_2 != null_id) or (edge.id_2 == null_id and edge.id_1 != null_id):
                has_at_least_one_edge = True
                break
        if not has_at_least_one_edge:
            self.new_graph.remove_node(null_id)

    def nfa_to_nfd(self):
        next_to_go = queue.Queue()
        next_to_go.put([self.graph.nodes[0]])
        estados_gone = set()

        while not next_to_go.empty():
            current_nodes = next_to_go.get()
            total_edges = [[] for _ in range(len(self.alpha))]

            estados_gone.add(self.convert_estado_to_string([estado.id for estado in current_nodes]))

            for current_node in current_nodes:
                for character in self.alpha:
                    int_equivalent = ord(character)-ord('a')

                    for i in range(len(current_node.adjs)):
                        adj = current_node.adjs[i]
                        edge = current_node.edges[i]

                        if edge == character:
                            if adj.id not in total_edges[int_equivalent]:
                                total_edges[int_equivalent].append(adj.id)

            for i in range(len(total_edges)):
                total_edges[i] = sorted(total_edges[i])

            self.add_estados_to_new_graph([aux_node.id for aux_node in current_nodes], total_edges)

            # Putting next element on the queue
            for i in range(len(self.alpha)):
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

        for id in new_ids:
            is_end = False
            for node in self.convert_string_to_estados(id):
                if node.is_end_node:
                    is_end = True
                    break
            if is_end:
                self.new_graph.get_node(id).is_end_node = True
                self.new_graph.get_node(id).shape = 'doublecircle'

        self.add_null_state_for_new_graph()
        self.remove_duplicate_edges_of_new_graph(self.new_graph)

        return self.new_graph
