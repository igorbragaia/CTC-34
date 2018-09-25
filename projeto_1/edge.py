class Edge:
    def __init__(self, id_1, id_2, label):
        self.id_1 = id_1
        self.id_2 = id_2
        self.label = label

    def print(self):
        print("On edge with label:", str(self.label), ", with id_1 = ", str(self.id_1), " and id_2 = ", self.id_2)