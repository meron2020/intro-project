import json

import json_manager
from collections import deque

from Processor import Processor
from DirectNeighborsFinder import DirectNeighborsFinder


class IndirectConnectionFinder:
    def __init__(self, preprocessed_flag, people_connections_path, maximal_distance=None, window_size=None,
                 threshold=None,
                 name_file=None, sentence_file=None,
                 words_to_remove_file_path=None, preprocessed_json_file_path=None):
        self.adjacency_list = {}  # Stores the adjacency list for indirect connections.

        # If using a preprocessed file, load connections directly from JSON
        if preprocessed_flag:
            preprocessed_json = json_manager.load_json_file(preprocessed_json_file_path)
            self.connections = preprocessed_json['Question 6']["Pair Matches"]

        else:
            words_to_remove = Processor.read_csv_file(words_to_remove_file_path)  # Read words to remove from text.
            self.sentences = Processor.read_csv_file(sentence_file, words_to_remove)  # Read sentences from file.
            Processor.clean_sentences(self.sentences, words_to_remove)  # Perform preprocessing on sentences.

            persons = Processor.read_csv_file(name_file)  # Read people from name file.
            for person in persons:
                person.clean(words_to_remove)  # Clean names from unwanted words.

            # Initializes DirectNeighborsFinder to establish direct connections between people.
            self.neighbors_finder = DirectNeighborsFinder(False, window_size, threshold, name_file=name_file,
                                                          sentence_file=sentence_file,
                                                          words_to_remove_file_path=words_to_remove_file_path)
            self.adjacency_list = self.restructure_adjacency_list()  # Convert connections into adjacency list format.
            self.restructure_adjacency_list()  # Ensures adjacency list is structured correctly.

            self.connections = json.loads(self.neighbors_finder.return_connections())["Question 6"][
                "Pair Matches"]  # Fetch direct connections.
            self.person_to_node = {}  # Maps each person to their respective node in the graph.

        self.people_connections = json_manager.load_json_file(people_connections_path)[
            "keys"]  # Load input pairs of people to check.
        self.maximal_distance = maximal_distance  # Maximum distance for indirect connection search.

    # The adjacency list is returned such that the keys are nodes but the pairs are strings so the keys are switched to
    # the cleaned name of the person rather than their node.
    def restructure_adjacency_list(self):
        adjacency_list = {}
        connections = self.neighbors_finder.find_connections()  # Finds connections between all persons.
        for person in connections.keys():
            adjacency_list[person.real_name.cleaned_data] = connections[person]  # Switches keys from nodes to strings.

        return adjacency_list

    # Function uses algorithm BFS to find out if two people are indirectly connected.
    def persons_indirectly_connected(self, person1, person2, maximum_distance):
        if person1 == person2:
            return True  # Edge case where the connection is the same person.

        visited = set()  # Keeps track of visited nodes to avoid cycles.
        queue = deque([(person1, 0)])  # Queue stores the current person and the distance it is from the origin.
        visited.add(person1)

        while queue:
            node, moves = queue.popleft()  # Remove the first node from the queue in a first in first out fashion.
            if moves > maximum_distance:
                continue  # Quit search if distance is bigger than maximum.

            for neighbor in self.adjacency_list[node]:
                if moves + 1 > maximum_distance:
                    continue# Iterate through all direct neighbors of the current person.
                if neighbor.payload.real_name.cleaned_data == person2:
                    return True  # If neighbor of current person being checked is wanted, return True.
                if neighbor.payload.real_name.cleaned_data not in visited:  # Make sure node has not already been visited.
                    visited.add(neighbor.payload.real_name.cleaned_data)
                    queue.append((neighbor.payload.real_name.cleaned_data,
                                  moves + 1))  # Add neighbor to queue with updated distance.
        return False  # Returns False if no path was found between the two persons.

    def find_indirect_connections(self):
        pair_matches = []
        # Iterates over every inputted pair of people
        for people_connection in self.people_connections:
            if self.persons_indirectly_connected(people_connection[0], people_connection[1],
                                                 self.maximal_distance):  # Checks if they are connected
                pair_matches.append([sorted([people_connection[0], people_connection[1]])[0],
                                     sorted([people_connection[0], people_connection[1]])[1],
                                     True])  # If so add the sorted pair with True as the connection variable
            else:
                pair_matches.append([sorted([people_connection[0], people_connection[1]])[0],
                                     sorted([people_connection[0], people_connection[1]])[1],
                                     False])  # Otherwise add the sorted pair with False as the connection variable

        return json.dumps({"Question 7": {"Pair Matches": sorted(pair_matches)}})  # Returns the found connections sorted.

    # Function finds if two people are indirectly connected at an **exact** fixed length.
    def persons_indirectly_fixed_length(self, person1, person2, fixed_length):
        if fixed_length == 0:
            return person1 == person2  # If no steps allowed, they must be the same person to be "connected."

        queue = deque([(person1, 0, {person1})])  # Queue stores (current person, steps taken, visited set).
        while queue:
            current, steps_taken, visited = queue.popleft()

            if steps_taken == fixed_length:
                if current == person2:
                    return True  # If correct steps taken and reached target, return True.
                continue  # Otherwise, stop searching further.

            for neighbor in self.adjacency_list[current]:  # Iterate over all neighbors.
                if neighbor.payload.real_name.cleaned_data in visited:
                    continue  # Skip already visited nodes to avoid cycles.

                updated_visited = visited | {neighbor.payload.real_name.cleaned_data}  # Update visited set.
                queue.append((neighbor.payload.real_name.cleaned_data, steps_taken + 1,
                              updated_visited))  # Add neighbor to queue.
        return False  # Returns False if no path of exact fixed length is found.

    def find_indirect_connections_fixed_length(self, fixed_length):
        pair_matches = []
        # Iterates over every pair of people in the input data.
        for people_connection in self.people_connections:
            if self.persons_indirectly_fixed_length(people_connection[0], people_connection[1], fixed_length):
                pair_matches.append([sorted([people_connection[0], people_connection[1]])[0],
                                     sorted([people_connection[0], people_connection[1]])[1],
                                     True])  # Add True if connected.
            else:
                pair_matches.append([sorted([people_connection[0], people_connection[1]])[0],
                                     sorted([people_connection[0], people_connection[1]])[1],
                                     False])  # Add False if not connected.

        return json.dumps({"Question 8": {"Pair Matches": sorted(pair_matches)}})  # Return sorted results in JSON format.
