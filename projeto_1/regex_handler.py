from graph import Graph
from node import Node


class RegexHandler:
    def __init__(self):
        self.expr = input("Digite a expressão regular aqui: ")
        self.graph = Graph()
        node_inicio = Node(0)
        node_final = Node(1)
        self.graph.add_node(node_inicio)
        self.graph.add_node(node_final)
        self.graph.add_edge(0, 1, self.expr)
        self.graph.print_graph()

    def check_running(self):
        running = False
        for edge in self.graph.edges:
            if len(edge.label) > 1:
                running = True
                break
            elif len(edge.label) < 1:
                print("Edge between id_1 = ", edge.id_1, " and id_2 = ", edge.id_2, " is empty")
        return running
