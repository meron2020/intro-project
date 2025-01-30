class Node:
    def __init__(self, person):
        self.person = person
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def check_node_is_neighbor(self, node):
        return node in self.neighbors

    def __eq__(self, other):
        return self.person == other.person and self.neighbors == other.neighbors

