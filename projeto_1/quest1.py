from regex_handler import RegexHandler
from graph import EpsilonNFAToNFA

if __name__ == "__main__":
    expr = input("Digite a expressão regular aqui: ")
    regex_handler = RegexHandler(expr)

    while regex_handler.check_running():
        regex_handler.check_union()
        regex_handler.check_concatenation()
        regex_handler.check_kleene()
        regex_handler.check_parentheses()
        # regex_handler.graph.print_edges()
    # regex_handler.graph.create_output()
    questao2 = EpsilonNFAToNFA(regex_handler.graph)
    regex_handler.graph.create_output()
