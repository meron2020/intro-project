import csv
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SentenceGrouper import SentenceGrouper
from Processor import Processor
from Node import Node


# Helper function: create a temporary CSV file with given rows.
def create_temp_csv(rows):
    temp = tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False, encoding="utf-8")
    writer = csv.writer(temp)
    for row in rows:
        writer.writerow(row)
    temp.close()
    return temp.name


# Helper function: create a temporary JSON file with provided content.
def create_temp_json(content):
    temp = tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8", suffix=".json")
    json.dump(content, temp)
    temp.close()
    return temp.name


# Helper function: create a dummy temporary JSON file.
def create_dummy_temp_json():
    return create_temp_json({})


# Dummy Sentence class to simulate similarity using a custom attribute "group".
class DummySentence:
    def __init__(self, text, word_list, group):
        self.data = text
        self.cleaned_data = text.lower()
        self.word_list = word_list
        self.group = group

    def sentence_is_similar(self, other, threshold):
        # Ignore threshold; sentences are similar if they have the same group.
        return self.group == other.group


# Test suite for SentenceGrouper
class TestSentenceGrouper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create dummy sentences for grouping.
        # Group 1: s1 and s2
        cls.s1 = DummySentence("alpha beta", ["alpha", "beta"], group=1)
        cls.s2 = DummySentence("alpha beta gamma", ["alpha", "beta", "gamma"], group=1)
        # Group 2: s3, s4, s5
        cls.s3 = DummySentence("delta epsilon", ["delta", "epsilon"], group=2)
        cls.s4 = DummySentence("delta epsilon zeta", ["delta", "epsilon", "zeta"], group=2)
        cls.s5 = DummySentence("delta epsilon theta", ["delta", "epsilon", "theta"], group=2)
        # Group 3: s6 (isolated)
        cls.s6 = DummySentence("iota kappa", ["iota", "kappa"], group=3)

        # List of dummy sentences (simulate preprocessed branch).
        cls.dummy_sentences = [cls.s1, cls.s2, cls.s3, cls.s4, cls.s5, cls.s6]
        # Dummy preprocessed JSON content.
        cls.preproc_dummy = {"Processed Sentences": cls.dummy_sentences}

        # Monkey-patch json_manager.load_json_file to return our dummy preprocessed JSON.
        import json_manager
        cls.orig_json_load = json_manager.load_json_file
        json_manager.load_json_file = lambda path: cls.preproc_dummy

    @classmethod
    def tearDownClass(cls):
        import json_manager
        json_manager.load_json_file = cls.orig_json_load

    # Test that the constructor loads preprocessed sentences correctly.
    def test_init_preprocessed_true(self):
        preproc_file = create_dummy_temp_json()
        sg = SentenceGrouper(preprocessed_flag=True,
                             threshold=2,
                             preprocessed_json_file_path=preproc_file)
        self.assertEqual(sg.sentences, self.dummy_sentences)
        os.remove(preproc_file)

    # Test that create_sentence_nodes creates one Node per sentence and initializes adjacency_list.
    def test_create_sentence_nodes(self):
        preproc_file = create_dummy_temp_json()
        sg = SentenceGrouper(preprocessed_flag=True,
                             threshold=2,
                             preprocessed_json_file_path=preproc_file)
        # The constructor already calls create_sentence_nodes
        self.assertEqual(len(sg.sentence_nodes), len(self.dummy_sentences))
        for node in sg.sentence_nodes:
            self.assertTrue(hasattr(node, "payload"))
            self.assertIn(node.payload, self.dummy_sentences)
        self.assertEqual(len(sg.adjacency_list), len(sg.sentence_nodes))
        os.remove(preproc_file)

    # Test that create_connections_between_sentences connects nodes with similar sentences.
    def test_create_connections_between_sentences(self):
        preproc_file = create_dummy_temp_json()
        sg = SentenceGrouper(preprocessed_flag=True,
                             threshold=2,
                             preprocessed_json_file_path=preproc_file)
        sg.create_sentence_nodes(sg.sentences)
        sg.create_connections_between_sentences(sg.sentence_nodes)
        # Build a helper dict mapping from cleaned_data to node.
        node_map = {node.payload.cleaned_data: node for node in sg.sentence_nodes}
        # For Group 1: s1 and s2 should be connected.
        self.assertIn(node_map[self.s2.cleaned_data], node_map[self.s1.cleaned_data].neighbors)
        # Ensure that a node from Group 1 is not connected to one from Group 2.
        self.assertFalse(any(neighbor.payload == self.s3 for neighbor in node_map[self.s1.cleaned_data].neighbors))
        os.remove(preproc_file)

    # Test that find_interconnected_groups finds groups correctly and return_groups produces sorted JSON output.
    def test_find_interconnected_groups_and_return_groups(self):
        preproc_file = create_dummy_temp_json()
        sg = SentenceGrouper(preprocessed_flag=True,
                             threshold=2,
                             preprocessed_json_file_path=preproc_file)
        groups = sg.find_interconnected_groups()
        self.assertEqual(len(groups), 3)  # Expect three groups
        sizes = sorted([len(group) for group in groups])
        self.assertEqual(sizes, [1, 2, 3])
        output_json = sg.return_groups(groups)
        output = json.loads(output_json)
        self.assertIn("Question 9", output)
        self.assertIn("group Matches", output["Question 9"])
        groups_output = output["Question 9"]["group Matches"]
        self.assertEqual(len(groups_output), 3)
        # Expected groups based on our dummy:
        expected_group1 = [["iota", "kappa"]]  # Group 3 (isolated s6)
        expected_group2 = sorted([["alpha", "beta"], ["alpha", "beta", "gamma"]])  # Group 1
        expected_group3 = sorted(
            [["delta", "epsilon"], ["delta", "epsilon", "theta"], ["delta", "epsilon", "zeta"]])  # Group 2
        expected_output = {
            "Question 9": {
                "group Matches": [
                    ["Group 1", expected_group1],
                    ["Group 2", expected_group2],
                    ["Group 3", expected_group3]
                ]
            }
        }
        self.assertEqual(output, expected_output)
        os.remove(preproc_file)


if __name__ == '__main__':
    unittest.main()
