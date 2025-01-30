from Node import Node
class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, u, v):
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)


