from graph import Graph


class SubstringsAccepted:
    def __init__(self, graph):
        # string = input("Digite a sub-cadeia a ser testada aqui: ")
        string = "abba"
        self.graph = graph
        self.substrings_accepted(string)

    def strings_accepted(self, chain):
        ids_possible_states = [0]
        ids_possible_states_aux = []
        for i in range(len(chain)):
            for current_id_possible_state in ids_possible_states:
                for j in range(len(self.graph.edges)):
                    if (self.graph.edges[j].id_1 == current_id_possible_state) and (chain[i] in self.graph.edges[j].label):
                        ids_possible_states_aux.append(self.graph.edges[j].id_2)
            ids_possible_states = []
            for j in ids_possible_states_aux:
                ids_possible_states.append(j)
            ids_possible_states_aux = []
        for i in ids_possible_states:
            if self.graph.nodes[i].shape == 'doublecircle':
                return True
        return False

    def substrings_accepted(self, chain):
        print("Sub-cadeias aceitas:")
        accepted_strings = []
        for i in range(len(chain) + 1):
            for j in range(len(chain) + 1):
                if j >= i:
                    subchain = chain[i:j]
                    accepted = self.strings_accepted(subchain)
                    if accepted and subchain not in accepted_strings:
                        accepted_strings.append(subchain)
        for subchain in accepted_strings:
            print(subchain)
