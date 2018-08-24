from graph import Graph
from node import Node


class RegexHandler:
    def __init__(self, expr):
        self.expr = expr
        self.graph = Graph()
        node_inicio = self.graph.create_node()
        node_final = self.graph.create_node(shape='doublecircle')
        self.graph.add_edge(node_inicio, node_final, self.expr)

    def check_running(self):
        running = False
        for edge in self.graph.edges:
            if len(edge.label) > 1:
                running = True
                break
            elif len(edge.label) < 1:
                print("Edge between id_1 = ", edge.id_1, " and id_2 = ", edge.id_2, " is empty")
        return running

    def check_union(self):
        for edge in self.graph.edges:
            found = True
            while found:
                number_of_oppened_parentheses = 0
                found = False
                for i in range(len(edge.label)):
                    char = edge.label[i]
                    if char == '(':
                        number_of_oppened_parentheses += 1
                    elif char == ')':
                        number_of_oppened_parentheses -= 1
                    elif char == '+' and number_of_oppened_parentheses == 0:
                        found = True
                        str_1 = edge.label[0:i]
                        str_2 = edge.label[i+1:]
                        # print("edge.label = ", edge.label, "str_1 = ", str_1, ", str_2 = ", str_2)
                        edge.label = str_1
                        self.graph.add_edge(edge.id_1, edge.id_2, str_2)
                        break

    def check_concatenation(self):
        for edge in self.graph.edges:
            found = True
            while found:
                number_of_oppened_parentheses = 0
                found = False
                for i in range(len(edge.label)):
                    char = edge.label[i]
                    if char == '(':
                        number_of_oppened_parentheses += 1
                    elif char == ')':
                        number_of_oppened_parentheses -= 1
                    elif char != '*' and number_of_oppened_parentheses == 0 and i != 0:
                        found = True
                        str_1 = edge.label[0:i]
                        str_2 = edge.label[i:]
                        print("edge.label = ", edge.label, "str_1 = ", str_1, ", str_2 = ", str_2)
                        node_id = self.graph.create_node()
                        edge.label = str_1
                        self.graph.add_edge(node_id, edge.id_2, str_2)
                        edge.id_2 = int(node_id)
                        break

    def check_kleene(self):
        aux_str = ""
        number_of_closed_parentheses = 0

        for edge in self.graph.edges:
            if edge.label[-1] == '*':
                if edge.label[-2] == ')':
                    for i in range(len(edge.label)-2, -1, -1):
                        # print("i = ", str(i), ", A[i] = " , edge.label[i])
                        if edge.label[i] == ')':
                            number_of_closed_parentheses += 1
                        elif edge.label[i] == '(':
                            number_of_closed_parentheses -= 1
                        if number_of_closed_parentheses == 0:
                            aux_str = edge.label[i+1:-2]
                            break
                else:
                    aux_str = edge.label[-2]
                node_id = self.graph.create_node()
                id_1 = int(edge.id_1)
                id_2 = int(edge.id_2)
                edge.id_1 = node_id
                edge.id_2 = node_id
                edge.label = aux_str
                self.graph.add_edge(id_1, node_id, "&")
                self.graph.add_edge(node_id, id_2, "&")

    def check_parentheses(self):
        for edge in self.graph.edges:
            if edge.label[0] == '(' and edge.label[-1] == ')':
                edge.label = edge.label[1:-1]
