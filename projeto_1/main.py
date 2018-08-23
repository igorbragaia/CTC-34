from graph import Graph
from node import Node

if __name__ == "__main__":
    graph = Graph()
    nodeA = Node(1)
    nodeB = Node(2)

    graph.add_node(nodeA)
    graph.print_graph()
    graph.add_node(nodeB)
    graph.print_graph()

    graph.add_edge(1, 2)
    graph.print_graph()

    graph.create_output()
