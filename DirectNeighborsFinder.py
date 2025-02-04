import json

import json_manager
from Node import Node
from Processor import Processor
from SentenceWindow import SentenceWindow


class DirectNeighborsFinder:
    def __init__(self, preprocessed_flag, window_size, threshold, name_file=None, sentence_file=None,
                 words_to_remove_file_path=None, preprocessed_json_file_path=None):
        self.adjacency_list = {}
        if preprocessed_flag:
            # Unpacks the sentences and people from the json that is in the same format as task 1
            preprocessed_json = json_manager.load_json_file(preprocessed_json_file_path)
            self.sentences = preprocessed_json["Question 1"]["Processed Sentences"]
            persons = preprocessed_json["Question 1"]["Persons"]
        else:
            # Executes the preprocessing cleaning procedure and sets the variables needed (sentences and persons)
            words_to_remove = Processor.read_csv_file(words_to_remove_file_path)
            self.sentences = Processor.read_csv_file(sentence_file, words_to_remove)
            Processor.clean_sentences(self.sentences, words_to_remove)
            persons = Processor.read_csv_file(name_file)
            for person in persons:
                person.clean(words_to_remove)

        # Sets instance variables.
        self.window_size = window_size
        self.threshold = threshold
        self.person_windows_dict = {}
        self.person_to_node = {}
        # Creates person nodes
        self.create_nodes(persons)
        # Find all windows each person is in and set the person_windows_dict dictionary.
        self.find_windows_person_in()

    # Iterates over persons, creates person nodes.
    def create_nodes(self, persons):
        for person in persons:
            self.adjacency_list[person] = []
            self.person_to_node[person] = Node(person)

    # Function iterates over each person and finds all sentence windows the person is in.
    def find_windows_person_in(self):
        for person in self.adjacency_list.keys():
            sentence_windows = []
            # Iterate over all windows and add window to list of windows if person is found in it.
            for i in range(len(self.sentences) - self.window_size + 1):
                sentence_window = SentenceWindow(self.sentences[i:i + self.window_size])
                if sentence_window.find_person_in_window(person):
                    sentence_windows.append(sentence_window)
            # No need to add person to dictionary if he is not found in any windows.
            if len(sentence_windows) > 0:
                self.person_windows_dict[person] = sentence_windows

    # Function finds the connections between all persons found in the text.
    def find_connections(self):
        # Iterates over every person that is found in the text.
        for person in self.person_windows_dict.keys():
            node = self.person_to_node[person]
            # Iterates over every other person
            for person_to_check in self.person_windows_dict.keys():
                node_to_check = self.person_to_node[person_to_check]
                # Make sure not to check against oneself.
                if not node_to_check == node:
                    similar_windows = 0
                    # Check how many of the persons sentence windows contain the other person.
                    for sentence_window in self.person_windows_dict[person]:
                        if sentence_window.find_person_in_window(node_to_check.payload):
                            similar_windows += 1
                    # If the amount of windows is at least the threshold, create the connection.
                    if similar_windows >= self.threshold:
                        if not node.check_node_is_neighbor(node_to_check):
                            node.add_neighbor(node_to_check)
                            node_to_check.add_neighbor(node)
                            self.adjacency_list[person].append(node_to_check)
                            self.adjacency_list[node_to_check.payload].append(self.person_to_node[person])

        # Returns a dictionary in which each node is a key and its value is a list of the nodes its connected to.
        return self.adjacency_list

    # Returns the connected pairs according to the format required.
    def return_connections(self):
        connections = []
        # Iterates over every person in the text
        for person in self.adjacency_list.keys():
            # Iterates over the person's neighbors
            for neighbor in self.adjacency_list[person]:
                # Checks if there are duplicate connections.
                if [neighbor.payload.real_name.word_list, person.real_name.word_list] not in connections:
                    connections.append([person.real_name.word_list,
                                        neighbor.payload.real_name.word_list])  # Adds connection to connections list.
        # Sort each pair internally
        sorted_pairs = [sorted(pair, key=lambda x: tuple(x)) for pair in connections]

        # Sort the list of pairs lexicographically based on the first element
        sorted_pairs = sorted(sorted_pairs, key=lambda x: (tuple(x[0]), tuple(x[1])))
        return json.dumps({"Question 6": {"Pair Matches": sorted_pairs}})
