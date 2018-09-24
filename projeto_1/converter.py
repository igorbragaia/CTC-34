from graph import Graph
from collections import deque


class Converter:
    def __init__(self, graph):
        self.graph = graph  # Is the NFA received graph
        self.new_graph = Graph()  # Will be the NFD graph
        pass

    def getPossivelEstado(self, proxEstado):
        possivelEstado = ""

        print("")
        print("proxEstado = " + str(proxEstado))

        for i in range(len(proxEstado)):  # Iterating throught the ids of proxEstado
            print("i = ", str(i))
            print(proxEstado[i])

            node = self.graph.get_node(proxEstado[i])
            if node is None:
                continue

            for c in range(3):
                print("On c = ", str(c))

                for adj in node.adjs:
                    edge = adj.edge

                    if edge == c:
                        print("In the if")
                        possivelEstado += str(c)

            possivelEstado = ''.join(sorted(possivelEstado))

            print("possivelEstado = ", str(possivelEstado))

            return possivelEstado
        return None

    def nfa_to_nfd(self):
        novosEstados = set()
        proxEstados = deque([str(self.graph.nodes[0].id)])

        self.graph.create_output()

        while proxEstados:  # While is not empty
            proxEstado = proxEstados[-1]
            proxEstados.popleft()
            novosEstados.add(proxEstado)

            possivelEstado = self.getPossivelEstado(proxEstado)

            if possivelEstado not in novosEstados and possivelEstado not in proxEstados \
                    and possivelEstado is not None and possivelEstado != '':
                proxEstados.appendleft(possivelEstado)

        print("")
        print("")
        print("Novos estados:")
        print(novosEstados)
