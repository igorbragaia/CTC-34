from __future__ import print_function


class StateReducer:
    def __init__(self, graph):
        self.graph = graph
        self.has_gone = []
        self.should_break = False

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
        begin_equal = self.are_begin_two_edges_equal(self.get_edges_that_begin_in_node(node_1),
                                               self.get_edges_that_begin_in_node(node_2))
        end_equal = self.are_end_two_edges_equal(self.get_edges_that_end_in_node(node_1),
                                             self.get_edges_that_end_in_node(node_2))
        contain_all_letter = True
        for c in node_1.id:
            if not c in node_2.id:
                contain_all_letter = False
                break
        if contain_all_letter and len(str(node_1.id)) > 1 and len(str(node_2.id)) > 1:
            end_equal = True

        return begin_equal and end_equal and node_1.is_end_node == node_2.is_end_node

    def merge_nodes(self, node_1, node_2):
        edge_end_2 = self.get_edges_that_end_in_node(node_2)

        for edge in edge_end_2:
            self.graph.add_edge(edge.id_1, node_1.id, edge.label)

        self.graph.remove_node(node_2.id)

    def DFS_of_end_nodes(self, current_node_id):
        if self.should_break:
            return
        has_at_least_one_diff = False
        self.has_gone.append(current_node_id)

        for i in range(len(self.graph.get_node(current_node_id).adjs)):
            adj = self.graph.get_node(current_node_id).adjs[i]

            if adj.is_end_node and adj.id not in self.has_gone:
                has_at_least_one_diff = True
                self.DFS_of_end_nodes(adj.id)

        is_a_circle = False
        if not has_at_least_one_diff:
            self.should_break = True
            for adj in self.graph.get_node(current_node_id).adjs:
                if adj.id in self.has_gone[:-1]:
                    is_a_circle = True
                    break
            if not is_a_circle:
                self.has_gone = []
        return

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
                        break
                if has_at_least_one_change:
                    break

        for node in self.graph.nodes:
            if node.is_end_node:
                self.DFS_of_end_nodes(node.id)
                break

        while len(self.has_gone) > 1:
            self.merge_nodes(self.graph.get_node(self.has_gone[0]), self.graph.get_node(self.has_gone[1]))
            del self.has_gone[1]

        return self.graph
