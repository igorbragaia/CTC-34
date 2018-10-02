from graph import Graph


class EpsilonNFAToNFAConverter:
    def __init__(self, graph):
        self.graph = graph  # Is the NFA received graph
        self.closures = {}

    def epsilon_nfa_to_nfa(self, id=0):
        self.__create_closures(id)
        self.__rewrite_graph()
        return self.graph

    def __create_closures(self, node):
        self.closures[node] = [node]
        neighbors = [edge for edge in self.graph.edges if edge.id_1 == node]
        for edge in neighbors:
            if edge.id_2 not in self.closures:
                self.__create_closures(edge.id_2)
            if edge.label == '&':
                self.closures[node].extend(self.closures[edge.id_2])

    def __rewrite_graph(self):
        edges = list(self.graph.edges)

        for edge in edges:
            if edge.label == '&':
                self.graph.remove_edge(edge.id_1, edge.id_2, edge.label)

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
                self.graph.nodes[node1].is_end_node = True
