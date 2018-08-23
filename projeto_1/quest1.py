from regex_handler import RegexHandler

if __name__ == "__main__":
    regex_handler = RegexHandler()

    while RegexHandler.check_running():
        pass

    regex_handler.graph.create_output()

