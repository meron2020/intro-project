import json_manager
from Graph import Graph
from collections import deque

from Node import Node
from Task_1.Processor import Processor
from Task_6.DirectNeighborsFinder import DirectNeighborsFinder


class IndirectConnectionFinder(Graph):
    def __init__(self, preprocessed_flag, people_connections_path, maximal_distance, window_size=None, threshold=None,
                 name_file=None, sentence_file=None,
                 words_to_remove_file_path=None, preprocessed_json=None):
        super().__init__()
        if preprocessed_flag:
            self.sentences = preprocessed_json["Processed Sentences"]
            persons = []
        else:
            words_to_remove = Processor.read_csv_file(words_to_remove_file_path)
            self.sentences = Processor.read_csv_file(sentence_file, words_to_remove)
            Processor.clean_sentences(self.sentences, words_to_remove)
            persons = Processor.read_csv_file(name_file)
            for person in persons:
                person.clean(words_to_remove)

            self.person_to_node = {}


            self.neighbors_finder = DirectNeighborsFinder(False, window_size, threshold, name_file=name_file,
                                                          sentence_file=sentence_file,
                                                          words_to_remove_file_path=words_to_remove_file_path)
            self.adjacency_list = self.restructure_adjacency_list()
            self.connections = self.neighbors_finder.return_connections()["Question 6"]["Pair Matches"]

        self.people_connections = json_manager.load_json_file(people_connections_path)["keys"]
        self.maximal_distance = maximal_distance

    def create_node_pairing(self, raw_pairing_list):
        for pair in raw_pairing_list:
            for name in pair:
                node_name = " ".join(name)
                node_added = False
                for person in self.person_to_node.keys():
                    if person == node_name:
                        node_added = True
                if not node_added:
                    self.person_to_node[node_name] = Node(node_name)

    def restructure_adjacency_list(self):
        adjacency_list = {}
        connections = self.neighbors_finder.find_connections()
        for person in connections.keys():
            adjacency_list[person.real_name.cleaned_data] = connections[person]

        return adjacency_list

    # Function to create graph if necessary
    def create_graph(self, pair_list):
        for pair in pair_list:
            if pair[0] in self.adjacency_list.keys():
                self.adjacency_list[pair[0]].append(pair[1])
            else:
                self.adjacency_list[pair[0]] = [pair[1]]
            if pair[1] in self.adjacency_list.keys():
                self.adjacency_list[pair[1]].append(pair[0])
            else:
                self.adjacency_list[pair[1]] = [pair[0]]

    # Function uses algorithm (check which) to find out if two people are indirectly connected.
    def persons_indirectly_connected(self, person1, person2, maximum_distance):
        if person1 == person2:
            return True

        queue = deque([(person1, 0)])
        while queue:
            node, moves = queue.popleft()
            if moves > maximum_distance:
                continue

            for neighbor in self.adjacency_list[person1]:
                if neighbor.person.real_name.cleaned_data == person2:
                    return True
                queue.append((neighbor, moves + 1))
        return False

    def find_indirect_connections(self):
        pair_matches = []
        for people_connection in self.people_connections:
            if self.persons_indirectly_connected(people_connection[0], self.people_connections[1], self.maximal_distance):
                pair_matches.append([people_connection[0], people_connection[1], True])
            else:
                pair_matches.append([people_connection[0], people_connection[1], False])

        return {"Question 7": {"Pair Matches":pair_matches}}
