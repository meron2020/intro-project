class Edge:
    def __init__(self, first_node, second_node):
        self.first_node = first_node
        self.second_node = second_node

    def __eq__(self, other):
        return (self.first_node == other.first_node and self.second_node == other.second_node) or (
                    self.first_node == other.second_node and self.second_node == other.first_node)
