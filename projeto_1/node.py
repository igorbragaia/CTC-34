import pprint


class Node:
    def __init__(self, id):
        self.id = id
        self.adjs = []

    def add_adj(self, other_node, edge_name):
        self.adjs.append(other_node)
        self.adjs[-1].edge = edge_name

    def print_adjs(self):
        print("On node: ", self.id)
        pprint(self.adjs)
