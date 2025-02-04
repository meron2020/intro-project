import json

import json_manager
from Node import Node
from Processor import Processor


class SentenceGrouper:
    def __init__(self, preprocessed_flag, threshold, sentence_file=None, words_to_remove_file_path=None,
                 preprocessed_json_file_path=None):
        self.threshold = threshold  # Minimum number of shared words for sentences to be considered similar.
        self.sentence_nodes = []  # Stores sentence nodes.
        self.adjacency_list = {}  # Stores sentence connections.

        if preprocessed_flag:
            # Loads preprocessed sentences if available.
            preprocessed_json = json_manager.load_json_file(preprocessed_json_file_path)
            self.sentences = preprocessed_json["Processed Sentences"]
        else:
            # Reads sentences and removes unwanted words.
            words_to_remove = Processor.read_csv_file(words_to_remove_file_path)
            self.sentences = Processor.read_csv_file(sentence_file, words_to_remove)

        self.create_sentence_nodes(self.sentences)  # Converts sentences into node objects.
        self.create_connections_between_sentences(self.sentence_nodes)  # Establishes connections based on similarity.

    def create_sentence_nodes(self, sentences: list) -> None:
        for sentence in sentences:
            sentence_node = Node(sentence)  # Wraps each sentence in a Node object.
            self.sentence_nodes.append(sentence_node)
            self.adjacency_list[sentence_node] = []  # Initializes adjacency list with empty lists.

    def create_connections_between_sentences(self, sentence_nodes: list) -> None:
        for node in sentence_nodes:
            for node_to_check in sentence_nodes:
                if node != node_to_check:  # Avoids self-connections.
                    if node.payload.sentence_is_similar(node_to_check.payload, self.threshold):  # Checks similarity.
                        node.add_neighbor(node_to_check)
                        node_to_check.add_neighbor(node)
                        self.adjacency_list[node].append(node_to_check)  # Stores connections.

    def find_interconnected_group(self, node: Node, group: list, visited: set) -> None:
        # Uses DFS with a stack to find all connected nodes.
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in group:
                visited.add(current)
                group.append(current)
                for neighbor in self.adjacency_list[current]:  # Adds unvisited neighbors to the stack.
                    if neighbor not in visited:
                        stack.append(neighbor)

    def find_interconnected_groups(self) -> list:
        visited: set = set()
        groups = []

        for node in self.adjacency_list.keys():
            if node not in visited:  # Ensures each node is only processed once.
                group: list = []
                self.find_interconnected_group(node, group, visited)  # Finds all nodes connected to the current node.
                groups.append(group)  # Adds the connected group to the list.
        return groups

    def return_groups(self, groups: list) -> str:
        list_to_return = []

        # Processes groups and sorts sentences within each group.
        for group in groups:
            list_of_sentences = [sentence_node.payload.word_list for sentence_node in group]

            # Sorts sentences alphabetically based on entire sentence, not just the first word.
            list_of_sentences = sorted(list_of_sentences)

            list_to_return.append(list_of_sentences)

        # Sorts groups first by size, then lexicographically by sentence order.
        list_to_return = sorted(list_to_return, key=lambda x: (len(x), tuple(map(tuple, x))))

        # Adds group numbering to the final output.
        for i in range(len(list_to_return)):
            group = ["Group " + str(i + 1), list_to_return[i]]
            list_to_return[i] = group

        return json.dumps({"Question 9": {"group Matches": list_to_return}})  # Returns final grouped sentences.
