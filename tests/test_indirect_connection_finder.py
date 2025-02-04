import json
import os
import sys
import tempfile
import unittest
from collections import deque
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from IndirectConnectionFinder import IndirectConnectionFinder
from Node import Node
from Person import Person


# --- Helper Functions ---

def create_temp_json(content):
    """
    Creates a temporary JSON file containing the given content.
    Returns the temporary file's name.
    """
    temp = tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8", suffix=".json")
    json.dump(content, temp)
    temp.close()
    return temp.name


def create_dummy_temp_json(content):
    """
    Creates a dummy temporary JSON file.
    This function is a thin wrapper around create_temp_json.
    Returns the temporary file's name.
    """
    return create_temp_json(content)


def create_dummy_people_connections_json(pairs):
    """
    Given a list of pairs (each a list of two names as strings), create a JSON object
    with a "keys" entry and write it to a temporary file.
    Returns the temporary file's name.
    """
    content = {"keys": pairs}
    return create_temp_json(content)


# --- Dummy Graph Setup ---

def build_dummy_graph():
    """
    Build a dummy graph as an adjacency list mapping a person's cleaned name (string)
    to a list of Node objects representing direct neighbors.

    The graph is as follows (undirected):
        alice -- bob -- charlie -- diana

    Returns:
        (graph, alice, bob, charlie, diana)
    where graph is a dictionary:
        {
            "alice": [Node(bob)],
            "bob": [Node(alice), Node(charlie)],
            "charlie": [Node(bob), Node(diana)],
            "diana": [Node(charlie)]
        }
    """
    # Create dummy Person objects. Assume cleaning converts names to lowercase.
    alice = Person("Alice", "Ally")
    bob = Person("Bob", "Bobby")
    charlie = Person("Charlie", "Chuck")
    diana = Person("Diana", "Di")
    for person in (alice, bob, charlie, diana):
        person.clean([])  # Ensure cleaned_data is set

    # Create Node objects.
    node_alice = Node(alice)
    node_bob = Node(bob)
    node_charlie = Node(charlie)
    node_diana = Node(diana)

    # Build undirected connections.
    # alice <-> bob
    node_alice.add_neighbor(node_bob)
    node_bob.add_neighbor(node_alice)
    # bob <-> charlie
    node_bob.add_neighbor(node_charlie)
    node_charlie.add_neighbor(node_bob)
    # charlie <-> diana
    node_charlie.add_neighbor(node_diana)
    node_diana.add_neighbor(node_charlie)

    # Build the graph: keys are cleaned names, values are lists of neighbor Nodes.
    graph = {
        alice.real_name.cleaned_data: [node_bob],
        bob.real_name.cleaned_data: [node_alice, node_charlie],
        charlie.real_name.cleaned_data: [node_bob, node_diana],
        diana.real_name.cleaned_data: [node_charlie]
    }
    return graph, alice, bob, charlie, diana


# --- Test Suite for IndirectConnectionFinder ---

class TestIndirectConnectionFinder(unittest.TestCase):

    def setUp(self):
        # Create a dummy people_connections file.
        self.people_connections_pairs = [
            ["alice", "bob"],
            ["alice", "diana"],
            ["bob", "diana"],
            ["alice", "charlie"],
            ["charlie", "diana"]
        ]
        self.people_connections_file = create_dummy_temp_json({"keys": self.people_connections_pairs})
        # Create a dummy preprocessed JSON file for connections (for preprocessed branch).
        self.dummy_preproc = {"Question 6": {"Pair Matches": []}}
        self.preproc_file = create_temp_json(self.dummy_preproc)
        # Instantiate IndirectConnectionFinder with preprocessed_flag=True.
        self.icf = IndirectConnectionFinder(
            preprocessed_flag=True,
            people_connections_path=self.people_connections_file,
            maximal_distance=3,
            preprocessed_json_file_path=self.preproc_file
        )
        # Build our dummy graph and assign it to the instance.
        self.graph, self.alice, self.bob, self.charlie, self.diana = build_dummy_graph()
        self.icf.adjacency_list = self.graph

    def tearDown(self):
        os.remove(self.people_connections_file)
        os.remove(self.preproc_file)

    # --- Test persons_indirectly_connected ---
    def test_persons_indirectly_connected(self):
        """
        Test persons_indirectly_connected for various pairs and maximal distances.

        In our dummy graph:
          - alice to bob: distance = 1
          - alice to charlie: distance = 2 (alice → bob → charlie)
          - alice to diana: distance = 3 (alice → bob → charlie → diana)
        """
        self.assertTrue(self.icf.persons_indirectly_connected("alice", "alice", 0))
        self.assertTrue(self.icf.persons_indirectly_connected("alice", "bob", 1))
        self.assertFalse(self.icf.persons_indirectly_connected("alice", "charlie", 1))
        self.assertTrue(self.icf.persons_indirectly_connected("alice", "charlie", 2))
        self.assertFalse(self.icf.persons_indirectly_connected("alice", "diana", 2))
        self.assertTrue(self.icf.persons_indirectly_connected("alice", "diana", 3))
        self.assertFalse(self.icf.persons_indirectly_connected("bob", "diana", 0))

    # --- Test persons_indirectly_fixed_length ---
    def test_persons_indirectly_fixed_length(self):
        """
        Test persons_indirectly_fixed_length for exact-length paths.

        In our dummy graph:
          - alice → bob: length 1
          - alice → charlie: length 2
          - alice → diana: length 3
          - For K=0, only the same person is considered connected.
        """
        self.assertTrue(self.icf.persons_indirectly_fixed_length("alice", "alice", 0))
        self.assertFalse(self.icf.persons_indirectly_fixed_length("alice", "bob", 0))
        self.assertTrue(self.icf.persons_indirectly_fixed_length("alice", "bob", 1))
        self.assertTrue(self.icf.persons_indirectly_fixed_length("alice", "charlie", 2))
        self.assertTrue(self.icf.persons_indirectly_fixed_length("alice", "diana", 3))
        self.assertFalse(self.icf.persons_indirectly_fixed_length("alice", "diana", 2))
        self.assertTrue(self.icf.persons_indirectly_fixed_length("bob", "diana", 2))
        self.assertFalse(self.icf.persons_indirectly_fixed_length("bob", "diana", 1))

    # --- Test find_indirect_connections ---
    def test_find_indirect_connections(self):
        """
        Test that find_indirect_connections returns a JSON string with the expected format.
        Using our dummy graph and a maximal distance of 3, all pairs in our people_connections file
        should be indirectly connected.
        """
        json_str = self.icf.find_indirect_connections()
        output = json.loads(json_str)
        expected_pairs = []
        for pair in self.people_connections_pairs:
            sorted_pair = sorted(pair)
            expected_pairs.append(sorted_pair + [True])
        expected_pairs = sorted(expected_pairs, key=lambda p: (p[0], p[1]))
        expected = {"Question 7": {"Pair Matches": expected_pairs}}
        self.assertEqual(output, expected)

    # --- Test find_indirect_connections_fixed_length ---
    def test_find_indirect_connections_fixed_length(self):
        """
        Test that find_indirect_connections_fixed_length returns a JSON string with the expected format.

        For a fixed length K=2:
          - In our dummy graph, the pair ["alice", "charlie"] is connected by a path of length 2 (alice → bob → charlie).
          - The pair ["bob", "diana"] is connected by a path of length 2 (bob → charlie → diana).
          - Other pairs are not connected by exactly length 2.
        """
        json_str = self.icf.find_indirect_connections_fixed_length(fixed_length=2)
        output = json.loads(json_str)
        expected_pairs = []
        for pair in self.people_connections_pairs:
            sorted_pair = sorted(pair)
            if sorted_pair == ["alice", "charlie"] or sorted_pair == ["bob", "diana"]:
                value = True
            else:
                value = False
            expected_pairs.append(sorted_pair + [value])
        expected_pairs = sorted(expected_pairs, key=lambda p: (p[0], p[1]))
        expected = {"Question 8": {"Pair Matches": expected_pairs}}
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
