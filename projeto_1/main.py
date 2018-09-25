from regex_handler import RegexHandler
from converter import Converter

if __name__ == "__main__":
    # expr = input("Digite a expressão regular aqui: ")
    expr = "a*b*"
    regex_handler = RegexHandler(expr)

    while regex_handler.check_running():
        regex_handler.check_union()
        regex_handler.check_concatenation()
        regex_handler.check_kleene()
        regex_handler.check_parentheses()

    # regex_handler.graph.create_output()

    regex_handler.graph.epsilon_nfa_to_nfa()
    regex_handler.graph.create_output()

    # string = input("Digite a sub-cadeia a ser testada aqui: ")

    # string = "abba"
    # regex_handler.graph.substrings_accepted(string)

    converter = Converter(regex_handler.graph)
    converter.nfa_to_nfd()

