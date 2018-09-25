class Node:
    def __init__(self, id, shape='circle'):
        self.id = id
        self.adjs = []
        self.edge = None
        self.shape = shape

    def add_adj(self, other_node, edge_name):
        self.adjs.append(other_node)
        self.adjs[-1].edge = edge_name

    def print_adjs(self):
        print("On node: ", self.id)

        for adj in self.adjs:
            print("adj = ", adj.id, " with edge = ", adj.edge)
        print("")
