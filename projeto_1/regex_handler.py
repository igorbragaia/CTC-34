from graph import Graph
from node import Node


class RegexHandler:
    def __init__(self, expr):
        self.expr = expr
        self.graph = Graph()
        node_inicio = Node(0)
        node_final = Node(1, shape='doublecircle')
        self.graph.add_node(node_inicio)
        self.graph.add_node(node_final)
        self.graph.add_edge(0, 1, self.expr)

    def check_running(self):
        running = False
        for edge in self.graph.edges:
            if len(edge.label) > 1:
                running = True
                break
            elif len(edge.label) < 1:
                print("Edge between id_1 = ", edge.id_1, " and id_2 = ", edge.id_2, " is empty")
        return running

    def check_union(self):
        pass

    def check_concatenation(self):

        pass

    def check_kleene(self):
        pass

    def check_parentheses(self):
        for edge in self.graph.edges:
            if edge.label[0] == '(' and edge.label[-1] == ')':
                edge.label = edge.label[1:-1]
