class StateReducer:
    def __init__(self, graph):
        self.graph = graph

    def get_edges_that_begin_in_node(self, node):
        edges = []
        for edge in self.graph.edges:
            if str(edge.id_1) == str(node.id):
                edges.append(edge)
        return edges

    def get_edges_that_end_in_node(self, node):
        edges = []
        for edge in self.graph.edges:
            if str(edge.id_2) == str(node.id):
                edges.append(edge)
        return edges

    def are_begin_two_edges_equal(self, edges_1, edges_2):
        if len(edges_1) != len(edges_2):
            return False

        equal = True
        for edge_1 in edges_1:
            edge_equal = False
            for edge_2 in edges_2:
                if edge_1.id_2 == edge_2.id_2 and edge_1.label == edge_2.label:
                    edge_equal = True
                    break
            if not edge_equal:
                equal = False
                break
        return equal

    def are_end_two_edges_equal(self, edges_1, edges_2):
        # if len(edges_1) != len(edges_2):
        #     return False

        equal = True
        for edge_1 in edges_1:
            edge_equal = False
            for edge_2 in edges_2:
                if (edge_1.id_1 == edge_2.id_1 or edge_1.id_2 == edge_2.id_1 or edge_2.id_1 == edge_1.id_2) \
                        and edge_1.label == edge_2.label:
                    edge_equal = True
                    break
            if not edge_equal:
                equal = False
                break
        return equal

    def check_equivalent_node(self, node_1, node_2):
        print("On check_equivalent_node, with node_1 = ", str(node_1.id), " and node_2 = ", str(node_2.id))
        print("self.get_edges_that_begin_in_node(node_1):")
        [edge.print() for edge in self.get_edges_that_begin_in_node(node_1)]
        print("self.get_edges_that_begin_in_node(node_2):")
        [edge.print() for edge in self.get_edges_that_begin_in_node(node_2)]

        begin_equal = self.are_begin_two_edges_equal(self.get_edges_that_begin_in_node(node_1),
                                               self.get_edges_that_begin_in_node(node_2))
        print("begin_equal = ", begin_equal)
        print("")

        print("self.get_edges_that_end_in_node(node_1):")
        [edge.print() for edge in self.get_edges_that_end_in_node(node_1)]

        print("self.get_edges_that_end_in_node(node_2):")
        [edge.print() for edge in self.get_edges_that_end_in_node(node_2)]

        end_equal = self.are_end_two_edges_equal(self.get_edges_that_end_in_node(node_1),
                                             self.get_edges_that_end_in_node(node_2))
        print("end_equal = ", end_equal)
        print("")
        print("")
        return begin_equal and end_equal

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
                        print("Node: ", str(node_1.id), " and node: ", str(node_2.id), " are equivalents")
                        has_at_least_one_change = True
                        self.merge_nodes(node_1, node_2)

        return self.graph