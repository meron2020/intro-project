import csv
import json
import os
import sys
import tempfile
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DirectNeighborsFinder import DirectNeighborsFinder
from Processor import Processor
from Node import Node
from SentenceWindow import SentenceWindow
from Person import Person
from Sentence import Sentence

# --- Helper Functions ---

def create_temp_csv(rows):
    # Creates a temporary CSV file with the provided rows (first row is header)
    temp = tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False, encoding="utf-8")
    writer = csv.writer(temp)
    for row in rows:
        writer.writerow(row)
    temp.close()
    return temp.name

def create_dummy_temp_json():
    # Creates a temporary JSON file with an empty object (its content is not used)
    temp = tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8", suffix=".json")
    temp.write("{}")
    temp.close()
    return temp.name

# Dummy override for SentenceWindow.find_person_in_window
def dummy_find_person_in_window(self, person):
    # Returns True if person's cleaned real name appears in any sentence's cleaned_data in the window
    return any(person.real_name.cleaned_data in sentence.cleaned_data for sentence in self.sentences)

# --- Test Suite for DirectNeighborsFinder ---

class TestDirectNeighborsFinder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create dummy Person objects and clean them so that cleaned_data is lowercase
        cls.person_alice = Person("Alice", "Ally")
        cls.person_bob = Person("Bob", "Bobby")
        cls.person_charlie = Person("Charlie", "Chuck")
        cls.person_alice.clean([])
        cls.person_bob.clean([])
        cls.person_charlie.clean([])

        # Create dummy Sentence objects with simple texts
        cls.sentence1 = Sentence("Alice and Bob", unwanted_words=[])
        cls.sentence2 = Sentence("Alice and Bob", unwanted_words=[])
        cls.sentence3 = Sentence("Alice and Charlie", unwanted_words=[])
        cls.sentence4 = Sentence("Bob and Charlie", unwanted_words=[])
        # After cleaning, e.g., cls.sentence1.cleaned_data should be "alice and bob"

        # Override SentenceWindow.find_person_in_window with our dummy implementation
        cls.orig_find_in_window = SentenceWindow.find_person_in_window
        SentenceWindow.find_person_in_window = dummy_find_person_in_window

    @classmethod
    def tearDownClass(cls):
        # Restore the original SentenceWindow.find_person_in_window
        SentenceWindow.find_person_in_window = cls.orig_find_in_window

    # Test for preprocessed branch: loads sentences and persons from JSON via monkey-patching.
    def test_init_preprocessed_true(self):
        dummy_json = {
            "Question 1": {
                "Processed Sentences": [self.sentence1, self.sentence2, self.sentence3, self.sentence4],
                "Persons": [self.person_alice, self.person_bob, self.person_charlie]
            }
        }
        preproc_file = create_dummy_temp_json()
        import json_manager
        orig_load = json_manager.load_json_file
        json_manager.load_json_file = lambda path: dummy_json
        try:
            dnf = DirectNeighborsFinder(
                preprocessed_flag=True,
                window_size=2,
                threshold=2,
                preprocessed_json_file_path=preproc_file
            )
            # Verify that sentences and persons are loaded
            self.assertEqual(dnf.sentences, dummy_json["Question 1"]["Processed Sentences"])
            # Check that nodes are created for each person (keys in adjacency_list)
            self.assertEqual(set(dnf.adjacency_list.keys()), set(dummy_json["Question 1"]["Persons"]))
        finally:
            json_manager.load_json_file = orig_load
            os.remove(preproc_file)

    # Test for non-preprocessed branch: loads data from CSV files.
    def test_init_preprocessed_false(self):
        sentences_csv = [
            ["sentence"],
            ["Alice and Bob"],
            ["Alice and Bob"],
            ["Alice and Charlie"],
            ["Bob and Charlie"]
        ]
        sentence_file = create_temp_csv(sentences_csv)
        persons_csv = [
            ["Name"],
            ["Alice", "Ally"],
            ["Bob", "Bobby"],
            ["Charlie", "Chuck"]
        ]
        name_file = create_temp_csv(persons_csv)
        common_csv = [
            ["common"],
            ["and"]  # "and" might be removed during cleaning
        ]
        common_file = create_temp_csv(common_csv)
        try:
            dnf = DirectNeighborsFinder(
                preprocessed_flag=False,
                window_size=2,
                threshold=2,
                sentence_file=sentence_file,
                name_file=name_file,
                words_to_remove_file_path=common_file
            )
            self.assertTrue(len(dnf.sentences) >= 1)
            self.assertTrue(all(hasattr(s, "word_list") for s in dnf.sentences))
            self.assertTrue(len(dnf.person_to_node) >= 1)
        finally:
            os.remove(sentence_file)
            os.remove(name_file)
            os.remove(common_file)

    # Test find_connections to verify correct neighbor connections are built.
    def test_find_connections(self):
        dummy_json = {
            "Question 1": {
                "Processed Sentences": [self.sentence1, self.sentence2, self.sentence3, self.sentence4],
                "Persons": [self.person_alice, self.person_bob, self.person_charlie]
            }
        }
        import json_manager
        orig_load = json_manager.load_json_file
        json_manager.load_json_file = lambda path: dummy_json
        try:
            dnf = DirectNeighborsFinder(
                preprocessed_flag=True,
                window_size=2,
                threshold=2,
                preprocessed_json_file_path="dummy.json"
            )
            adjacency = dnf.find_connections()
            # Retrieve nodes from person_to_node mapping.
            node_alice = dnf.person_to_node[self.person_alice]
            node_bob = dnf.person_to_node[self.person_bob]
            node_charlie = dnf.person_to_node[self.person_charlie]
            self.assertIn(node_bob, node_alice.neighbors)
            self.assertIn(node_charlie, node_alice.neighbors)
            self.assertIn(node_alice, node_bob.neighbors)
            self.assertIn(node_charlie, node_bob.neighbors)
            self.assertIn(node_alice, node_charlie.neighbors)
            self.assertIn(node_bob, node_charlie.neighbors)
        finally:
            json_manager.load_json_file = orig_load

    # Test return_connections to verify the JSON output format and sorted connections.
    def test_return_connections(self):
        dummy_json = {
            "Question 1": {
                "Processed Sentences": [self.sentence1, self.sentence2, self.sentence3, self.sentence4],
                "Persons": [self.person_alice, self.person_bob, self.person_charlie]
            }
        }
        import json_manager
        orig_load = json_manager.load_json_file
        json_manager.load_json_file = lambda path: dummy_json
        try:
            dnf = DirectNeighborsFinder(
                preprocessed_flag=True,
                window_size=2,
                threshold=2,
                preprocessed_json_file_path="dummy.json"
            )
            dnf.find_connections()
            json_str = dnf.return_connections()
            output = json.loads(json_str)
            # Expected connections: pairs of persons (using their real_name.word_list)
            expected_pairs = [
                [self.person_alice.real_name.word_list, self.person_bob.real_name.word_list],
                [self.person_alice.real_name.word_list, self.person_charlie.real_name.word_list],
                [self.person_bob.real_name.word_list, self.person_charlie.real_name.word_list]
            ]
            expected = {"Question 6": {"Pair Matches": sorted(expected_pairs, key=lambda pair: (tuple(pair[0]), tuple(pair[1])))}}
            self.assertEqual(output, expected)
        finally:
            json_manager.load_json_file = orig_load

if __name__ == '__main__':
    unittest.main()
