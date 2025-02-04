class Node:
    def __init__(self, payload):
        self.payload = payload
        self.neighbors = []

    # Function adds a node to the neighbor instance variable list
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    # Function takes a node as an input and checks if it is a neighbor
    def check_node_is_neighbor(self, node):
        return node in self.neighbors

    # Defines how to check if two nodes are the same.
    def __eq__(self, other):
        return self.payload == other.payload and self.neighbors == other.neighbors

    # Function that returns a hash allowing the Node to be used as keys in dictionaries.
    def __hash__(self):
        return hash(self.payload)
