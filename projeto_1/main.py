from regex_handler import RegexHandler


if __name__ == "__main__":
    expr = input("Digite a expressão regular aqui: ")
    regex_handler = RegexHandler(expr)

    while regex_handler.check_running():
        regex_handler.check_union()
        regex_handler.check_concatenation()
        regex_handler.check_kleene()
        regex_handler.check_parentheses()
        # regex_handler.graph.print_edges()

    regex_handler.graph.epsilon_nfa_to_nfa()
    regex_handler.graph.create_output()
    regex_handler.graph.string_accepted("abb")
