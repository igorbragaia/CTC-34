import pprint


class Node:
    def __init__(self, id):
        self.id = id
        self.adjs = []
        self.edge = None

    def add_adj(self, other_node, edge_name):
        self.adjs.append(other_node)
        self.adjs[-1].edge = edge_name

    def print_adjs(self):
        print("On node: ", self.id)
        print(self.adjs)
