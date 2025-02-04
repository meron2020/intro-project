import csv
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from SequenceCounter import SequenceCounter
from Sentence import Sentence
from Processor import Processor

# Helper function to create a temporary file with given content.
def create_temp_file(content):
    temp = tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8")
    temp.write(content)
    temp.close()
    return temp.name

# Dummy implementation for create_sequence_list to use in tests.
def dummy_create_sequence_list(k, sentences):
    sequences = []
    for sentence in sentences:
        words = sentence.cleaned_data.split()
        if len(words) >= k:
            sequences.append(" ".join(words[:k]))
    return sequences

# Test suite for SequenceCounter
class TestSequenceCounter(unittest.TestCase):

    # Test that create_seq_list_for_sentence returns the correct sequences for a single sentence.
    def test_create_seq_list_for_sentence(self):
        sentence = Sentence("a b c", unwanted_words=[])
        expected = ["a b", "b c"]
        result = SequenceCounter.create_seq_list_for_sentence(2, sentence)
        self.assertEqual(result, expected)

    # Test that create_sequence_list returns the concatenated sequences from multiple sentences.
    def test_create_sequence_list(self):
        s1 = Sentence("a b", unwanted_words=[])
        s2 = Sentence("c d e", unwanted_words=[])
        expected = ["a", "b", "c", "d", "e"]
        result = SequenceCounter.create_sequence_list(1, [s1, s2])
        self.assertEqual(result, expected)

    # Test that count_each_sequence returns a dictionary mapping sequences to their counts.
    def test_count_each_sequence(self):
        seq_list = ["a", "b", "a", "c", "b"]
        expected = {"a": 2, "b": 2, "c": 1}
        result = SequenceCounter.count_each_sequence(seq_list)
        self.assertEqual(result, expected)

    # Test that turn_dict_to_list converts a dictionary to a sorted list of [key, value] pairs.
    def test_turn_dict_to_list(self):
        seq_dict = {"b": 2, "a": 1, "c": 3}
        expected = [["a", 1], ["b", 2], ["c", 3]]
        result = SequenceCounter.turn_dict_to_list(seq_dict)
        self.assertEqual(result, expected)

    # Test that create_final_dictionary produces the correct JSON structure for a simple case.
    def test_create_final_dictionary(self):
        s1 = Sentence("a b a", unwanted_words=[])
        s2 = Sentence("b c", unwanted_words=[])
        json_str = SequenceCounter.create_final_dictionary(1, [s1, s2])
        result = json.loads(json_str)
        self.assertIn("Question 2", result)
        q2 = result["Question 2"]
        self.assertIn("1-Seq Counts", q2)
        final_list = q2["1-Seq Counts"]
        self.assertEqual(len(final_list), 1)
        key, seq_list = final_list[0]
        self.assertEqual(key, "1_seq")
        expected_seq_list = [["a", 2], ["b", 2], ["c", 1]]
        self.assertEqual(seq_list, expected_seq_list)

    # Test that the constructor loads data from a preprocessed JSON when the flag is True.
    def test_init_preprocessed_true(self):
        s1 = Sentence("hello world", unwanted_words=[])
        s2 = Sentence("test sentence", unwanted_words=[])
        dummy_json = {"Question 1": {"Processed Sentences": [s1, s2]}}
        import json_manager
        orig_load = json_manager.load_json_file
        json_manager.load_json_file = lambda fp: dummy_json
        try:
            sc = SequenceCounter(preprocessed_flag=True, preprocessed_json_file_path="dummy.json")
            self.assertEqual(sc.sentences, [s1, s2])
        finally:
            json_manager.load_json_file = orig_load

    # Test that the constructor loads data from CSV files when the preprocessed flag is False.
    def test_init_preprocessed_false(self):
        s1 = Sentence("dummy sentence one", unwanted_words=[])
        s2 = Sentence("dummy sentence two", unwanted_words=[])
        dummy_sentences = [s1, s2]
        dummy_common = ["dummy"]
        orig_read_csv = Processor.read_csv_file
        orig_clean_sentences = Processor.clean_sentences
        Processor.read_csv_file = lambda file_path, unwanted_words=None: dummy_sentences if "sentence" in file_path else dummy_common
        Processor.clean_sentences = lambda sentences, common_words: None
        try:
            sc = SequenceCounter(preprocessed_flag=False, sentence_file="sentences.csv", words_to_remove_file_path="common.csv")
            self.assertEqual(sc.sentences, dummy_sentences)
        finally:
            Processor.read_csv_file = orig_read_csv
            Processor.clean_sentences = orig_clean_sentences

if __name__ == '__main__':
    unittest.main()
