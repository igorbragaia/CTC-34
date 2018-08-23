from graph import Graph
from node import Node
from regex_handler import RegexHandler

if __name__ == "__main__":
    regex_handler = RegexHandler()

    graph = Graph()
    node_inicio = Node(0)
    node_final = Node(1)



    graph.add_node(node_inicio)
    graph.print_graph()
    graph.add_node(node_final)
    graph.print_graph()

    graph.add_edge(0, 1, "kss")
    graph.add_edge(1, 0, "kiddeideio")
    graph.print_graph()

    graph.create_output()
