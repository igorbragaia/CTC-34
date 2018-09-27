from regex_handler import RegexHandler
from nfa_to_nfd_converter import NFAToNFDConverter
from epsilon_nfa_to_nfa_converter import EpsilonNFAToNFAConverter
from substrings_accepted import SubstringsAccepted
from substrings_accepted import SubstringsAccepted
from state_reducer import StateReducer

if __name__ == "__main__":
    # expr = input("Digite a expressão regular aqui: ")
    expr = "a*b*c*"
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

    # SubstringsAccepted(nfa_graph)

    nfa_to_nfd_converter = NFAToNFDConverter(nfa_graph)
    nfd_graph = nfa_to_nfd_converter.nfa_to_nfd()
    # nfd_graph.create_output()

    state_reducer = StateReducer(nfd_graph)
    reduced_graph = state_reducer.reduce_graph()
    reduced_graph.create_output()