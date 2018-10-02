class Node:
    def __init__(self, id, shape='circle'):
        self.initial = False
        self.id = id
        self.adjs = []
        self.edges = []
        self.shape = shape
        self.is_end_node = False
        if shape == 'doublecircle':
            self.is_end_node = True

    def add_adj(self, other_node, edge_name):
        self.adjs.append(other_node)
        self.edges.append(edge_name)

    def print_adjs(self):
        print("On node: ", self.id)

        for adj in self.adjs:
            print("adj = ", adj.id, " with edge = ", adj.edge)
        print("")
