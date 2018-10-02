from regex_handler import RegexHandler
from nfa_to_nfd_converter import NFAToNFDConverter
from epsilon_nfa_to_nfa_converter import EpsilonNFAToNFAConverter
from state_reducer import StateReducer


def create_automata_from_regex(min_state=False):
    expr = input("Digite a expressão regular aqui: ")
    regex_handler = RegexHandler(expr)

    while regex_handler.check_running():
        regex_handler.check_union()
        regex_handler.check_concatenation()
        regex_handler.check_kleene()
        regex_handler.check_parentheses()

    # regex_handler.graph.create_output()

    epsilon_nfa_to_nfa_converter = EpsilonNFAToNFAConverter(regex_handler.graph)
    nfa_graph = epsilon_nfa_to_nfa_converter.epsilon_nfa_to_nfa()
    # nfa_graph.create_output()

    if min_state is False:
        return nfa_graph

    nfa_to_nfd_converter = NFAToNFDConverter(nfa_graph)
    nfd_graph = nfa_to_nfd_converter.nfa_to_nfd(id=0)
    # nfd_graph.create_output()
    # return nfd_graph

    state_reducer = StateReducer(nfd_graph)
    reduced_graph = state_reducer.reduce_graph()

    return reduced_graph
    # nfd_graph.create_output()


def union_automata(reduced_graph1, reduced_graph_2):
    final_automata = reduced_graph1
    node_id2 = {}
    for node in reduced_graph_2.nodes:
        id2 = final_automata.create_node(shape=node.shape)
        node_id2[node.id] = id2
    for edge in reduced_graph_2.edges:
        final_automata.add_edge(node_id2[edge.id_1], node_id2[edge.id_2], edge.label)

    id_initial = final_automata.create_node(shape='circle')
    final_automata.add_edge(id_initial, 0, '&')
    final_automata.add_edge(id_initial, node_id2[0], '&')

    #final_automata.create_output()

    epsilon_nfa_to_nfa_converter = EpsilonNFAToNFAConverter(final_automata)
    nfa_graph = epsilon_nfa_to_nfa_converter.epsilon_nfa_to_nfa(id=id_initial)
    #nfa_graph.create_output()

    nfa_to_nfd_converter = NFAToNFDConverter(nfa_graph)
    nfd_graph = nfa_to_nfd_converter.nfa_to_nfd(id=id_initial)
    #nfd_graph.create_output()

    state_reducer = StateReducer(nfd_graph)
    reduced_graph = state_reducer.reduce_graph()
    #reduced_graph.create_output()

    return reduced_graph

def complement_automata(graph):
    new_nodes = []
    for node in graph.nodes:
        if node.shape == 'circle':
            node.shape = 'doublecircle'
            node.is_end_node = True
        else:
            node.shape = 'circle'
            node.is_end_node = False
        new_nodes.append(node)
    graph.nodes = new_nodes
    return graph


def intersect_automata(reduced_graph1, reduced_graph2):
    reduced_graph1 = complement_automata(reduced_graph1)
    reduced_graph2 = complement_automata(reduced_graph2)

    final_automata = union_automata(reduced_graph1, reduced_graph2)

    final_automata = complement_automata(final_automata)

    return final_automata


if __name__ == "__main__":
    # test with "(aa)*"
    automata1 = create_automata_from_regex(min_state=False)
    # test with "(aaa)*"
    automata2 = create_automata_from_regex(min_state=False)

    # automata1.create_output()
    # automata2.create_output()

    # final_automata = union_automata(automata1, automata2)

    # final_automata = complement_automata(automata1)
    # final_automata = complement_automata(automata2)

    final_automata = intersect_automata(automata1, automata2)

    final_automata.create_output()
