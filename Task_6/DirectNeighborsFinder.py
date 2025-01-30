from Graph import Graph
from Node import Node
from Task_1.Processor import Processor
from Task_6.SentenceWindow import SentenceWindow


class DirectNeighborsFinder(Graph):
    def __init__(self, preprocessed_flag, window_size, threshold, name_file=None, sentence_file=None,
                 words_to_remove_file_path=None, preprocessed_json=None):
        super().__init__()
        self.sentence_list = []
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
        self.window_size = window_size
        self.threshold = threshold
        self.person_windows_dict = {}
        self.person_to_node = {}
        self.create_nodes(persons)

        self.find_windows_person_in()

    # Iterates over persons, creates person nodes.
    def create_nodes(self, persons):
        for person in persons:
            self.adjacency_list[person] = []
            self.person_to_node[person] = Node(person)

    # Iterates over each node and creates the connections.
    def find_windows_person_in(self):
        for person in self.adjacency_list.keys():
            sentence_windows = []
            for i in range(len(self.sentences) - self.window_size + 1):
                sentence_window = SentenceWindow(self.sentences[i:i + self.window_size])
                if sentence_window.find_person_in_window(person):
                    sentence_windows.append(sentence_window)
            if len(sentence_windows) > 0:
                self.person_windows_dict[person] = sentence_windows

    def find_connections(self):
        for person, node in self.person_to_node.items():
            print(person.real_name)
            for person_to_check, node_to_check in self.person_to_node.items():
                if not node_to_check == node:
                    similar_windows = 0
                    if person in self.person_windows_dict.keys():
                        for sentence_window in self.person_windows_dict[person]:
                            if sentence_window.find_person_in_window(node_to_check.person):
                                similar_windows += 1
                        if similar_windows >= self.threshold:
                            if not node.check_node_is_neighbor(node_to_check):
                                node.add_neighbor(node_to_check)
                                node_to_check.add_neighbor(node)
                                self.adjacency_list[person].append(node_to_check)

        return self.adjacency_list

    def return_connections(self):
        connections = []
        for person in self.adjacency_list.keys():
            for person_to_check in self.adjacency_list:
                if self.person_to_node[person_to_check] in self.adjacency_list[person] and [person_to_check.real_name.word_list,
                                                                   person.real_name.word_list] not in connections:
                    connections.append([person.real_name.word_list, person_to_check.real_name.word_list])
        # Step 1: Sort each pair internally
        sorted_pairs = [sorted(pair, key=lambda x: tuple(x)) for pair in connections]

        # Step 2: Sort the list of pairs lexicographically based on the first element
        sorted_pairs = sorted(sorted_pairs, key=lambda x: (tuple(x[0]), tuple(x[1])))
        return {"Question 6": {"Pair Matches": sorted_pairs}}
