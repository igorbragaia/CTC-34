class StateReducer:
    def __init__(self, graph):
        self.graph = graph

    def check_equivalent_node(self, node_1, node_2):
        are_equivalent = True

        for edge in self.graph.edges:
            pass
        return are_equivalent

    def merge_nodes(self, node_1, node_2):
        pass

    def reduce_graph(self):
        has_at_least_one_change = True
        graph = self.graph
        while has_at_least_one_change:
            has_at_least_one_change = False

            for i in range(len(graph.nodes)):
                node_1 = graph.nodes[i]
                j = i+1
                while j < len(graph.nodes):
                    node_2 = graph.nodes[j]
                    j += 1
                    equivalents = self.check_equivalent_node(node_1, node_2)

                    if equivalents:
                        has_at_least_one_change = True
                        self.merge_nodes(node_1, node_2)


        return self.graph