import csv
import json
import os
import sys
import tempfile
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ContextFinder import ContextFinder
from Person import Person
from Sentence import Sentence
from Processor import Processor
from SequenceCounter import SequenceCounter

# --- Helper Functions ---

def create_temp_csv(rows):
    # Creates a temporary CSV file; first row is the header.
    temp = tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False, encoding="utf-8")
    writer = csv.writer(temp)
    for row in rows:
        writer.writerow(row)
    temp.close()
    return temp.name

def create_dummy_temp_json():
    # Creates a temporary JSON file with valid JSON content (an empty object).
    temp = tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8", suffix=".json")
    temp.write("{}")
    temp.close()
    return temp.name

# --- Test Suite for ContextFinder ---

class TestContextFinder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create dummy Person objects and clean them.
        cls.person_alice = Person("Alice", "Ally")
        cls.person_bob = Person("Bob", "Bobby")
        cls.person_alice.clean([])
        cls.person_bob.clean([])
        # Create dummy Sentence objects.
        cls.sentence1 = Sentence("Alice went home", unwanted_words=[])
        cls.sentence2 = Sentence("Bob went to the market", unwanted_words=[])
        cls.sentence3 = Sentence("Alice and Bob met", unwanted_words=[])
        cls.sentence4 = Sentence("Charlie is not here", unwanted_words=[])
        # Override check_if_person_in_sentence for controlled behavior.
        cls.sentence1.check_if_person_in_sentence = lambda person: (person.real_name.cleaned_data == "alice")
        cls.sentence3.check_if_person_in_sentence = lambda person: (person.real_name.cleaned_data in ["alice", "bob"])
        cls.sentence2.check_if_person_in_sentence = lambda person: (person.real_name.cleaned_data == "bob")
        cls.sentence4.check_if_person_in_sentence = lambda person: False
        # Override SequenceCounter.create_sequence_list with dummy implementation.
        cls.orig_create_seq = SequenceCounter.create_sequence_list
        def dummy_create_sequence_list(k, sentences):
            sequences = []
            for sentence in sentences:
                words = sentence.cleaned_data.split()
                if len(words) >= k:
                    sequences.append(" ".join(words[:k]))
            return sequences
        SequenceCounter.create_sequence_list = dummy_create_sequence_list

    @classmethod
    def tearDownClass(cls):
        SequenceCounter.create_sequence_list = cls.orig_create_seq

    # Test that __init__ loads sentences and persons from preprocessed JSON.
    def test_init_preprocessed_true(self):
        dummy_json = {
            "Question 1": {
                "Processed Sentences": [self.sentence1, self.sentence2, self.sentence3, self.sentence4],
                "Persons": [self.person_alice, self.person_bob]
            }
        }
        preproc_file = create_dummy_temp_json()
        import json_manager
        orig_load = json_manager.load_json_file
        json_manager.load_json_file = lambda path: dummy_json
        try:
            cf = ContextFinder(preprocessed_flag=True,
                                preprocessed_json_file_path=preproc_file)
            self.assertEqual(cf.sentences, dummy_json["Question 1"]["Processed Sentences"])
            self.assertEqual(cf.persons, dummy_json["Question 1"]["Persons"])
        finally:
            json_manager.load_json_file = orig_load
            os.remove(preproc_file)

    # Test that __init__ loads data from CSV files when preprocessed_flag is False.
    def test_init_preprocessed_false(self):
        sentences_data = [
            ["sentence"],
            ["Alice went home"],
            ["Alice and Bob met"],
            ["Bob went to the market"],
            ["Charlie is not here"]
        ]
        sentence_file = create_temp_csv(sentences_data)
        persons_data = [
            ["Name"],
            ["Alice", "Ally"],
            ["Bob", "Bobby"]
        ]
        name_file = create_temp_csv(persons_data)
        common_data = [
            ["common"],
            ["is"],
            ["not"]
        ]
        common_file = create_temp_csv(common_data)
        try:
            cf = ContextFinder(preprocessed_flag=False,
                                sentence_file=sentence_file,
                                name_file=name_file,
                                words_to_remove_file_path=common_file)
            self.assertTrue(len(cf.sentences) >= 1)
            self.assertTrue(all(hasattr(s, "word_list") for s in cf.sentences))
            self.assertTrue(len(cf.persons) >= 1)
            self.assertTrue(all(hasattr(p, "real_name") for p in cf.persons))
        finally:
            os.remove(sentence_file)
            os.remove(name_file)
            os.remove(common_file)

    # Test find_context returns unique k-sequences for a given person.
    def test_find_context(self):
        dummy_json = {
            "Question 1": {
                "Processed Sentences": [self.sentence1, self.sentence2, self.sentence3, self.sentence4],
                "Persons": [self.person_alice, self.person_bob]
            }
        }
        import json_manager
        orig_load = json_manager.load_json_file
        json_manager.load_json_file = lambda path: dummy_json
        try:
            cf = ContextFinder(preprocessed_flag=True, preprocessed_json_file_path="dummy.json")
            context = cf.find_context(self.person_alice, max_length=2)
            expected = sorted([
                ["alice"],
                ["alice", "and"],
                ["alice", "went"]
            ])
            self.assertEqual(context, expected)
        finally:
            json_manager.load_json_file = orig_load

    # Test find_all_contexts returns JSON with expected sorted structure.
    def test_find_all_contexts(self):
        dummy_json = {
            "Question 1": {
                "Processed Sentences": [self.sentence1, self.sentence2, self.sentence3, self.sentence4],
                "Persons": [self.person_alice, self.person_bob]
            }
        }
        import json_manager
        orig_load = json_manager.load_json_file
        json_manager.load_json_file = lambda path: dummy_json
        try:
            cf = ContextFinder(preprocessed_flag=True, preprocessed_json_file_path="dummy.json")
            output_json = cf.find_all_contexts(max_length=2)
            output = json.loads(output_json)
            # For Alice: expected k-seqs: [["alice"], ["alice", "and"], ["alice", "went"]]
            alice_seqs = sorted([["alice"], ["alice", "and"], ["alice", "went"]])
            # For Bob: expected k-seqs: [["bob"], ["bob", "went"], ["alice"], ["alice", "and"]]
            bob_seqs = sorted([["alice"], ["alice", "and"], ["bob"], ["bob", "went"]])
            expected_list = [
                [self.person_alice.real_name.cleaned_data, alice_seqs],
                [self.person_bob.real_name.cleaned_data, bob_seqs]
            ]
            expected = {"Question 5": {"Person Contexts and K-Seqs": expected_list}}
            self.assertEqual(output, expected)
        finally:
            json_manager.load_json_file = orig_load

if __name__ == '__main__':
    unittest.main()
