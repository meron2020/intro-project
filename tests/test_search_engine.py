import csv
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SearchEngine import SearchEngine
from Processor import Processor
from Sentence import Sentence
from Data import Data  # In case we need to construct Data objects


# --- Helper Functions ---

def create_temp_csv(data_rows):
    # Creates a temporary CSV file; first row is the header.
    temp_file = tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False, encoding="utf-8")
    writer = csv.writer(temp_file)
    for row in data_rows:
        writer.writerow(row)
    temp_file.close()
    return temp_file.name


def create_temp_json(content):
    # Creates a temporary JSON file with the given content.
    temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8", suffix=".json")
    json.dump(content, temp_file)
    temp_file.close()
    return temp_file.name


# --- Test Suite for SearchEngine ---

class TestSearchEngine(unittest.TestCase):

    # Test __init__ with preprocessed_flag True.
    def test_init_preprocessed_true(self):
        # Dummy sequences JSON with valid "keys".
        dummy_seq = {"keys": [["hello", "world"], ["test", "sequence"]]}
        seq_json_file = create_temp_json(dummy_seq)
        # Dummy preprocessed JSON for sentences.
        dummy_preprocessed = {
            "Question 1": {
                "Processed Sentences": [
                    Sentence("Hello world, this is a test.", unwanted_words=[]),
                    Sentence("Another test sequence appears here.", unwanted_words=[]),
                    Sentence("No match in this sentence.", unwanted_words=[])
                ]
            }
        }
        # Monkey-patch json_manager.load_json_file.
        import json_manager
        orig_load = json_manager.load_json_file
        json_manager.load_json_file = lambda path: dummy_preprocessed if "preprocessed" in path else dummy_seq
        try:
            engine = SearchEngine(
                seq_json_path=seq_json_file,
                preprocessed_flag=True,
                preprocessed_json_file_path="dummy_preprocessed.json"
            )
            expected_sequences = ["hello world", "test sequence"]
            self.assertEqual(engine.sequence_list, expected_sequences)
            self.assertEqual(engine.sentences, dummy_preprocessed["Question 1"]["Processed Sentences"])
        finally:
            json_manager.load_json_file = orig_load
            os.remove(seq_json_file)

    # Test __init__ with preprocessed_flag False.
    def test_init_preprocessed_false(self):
        # Dummy sequences JSON with valid "keys" to satisfy the constructor.
        dummy_seq = {"keys": [["hello", "world"], ["test", "sequence"]]}
        seq_json_path = create_temp_json(dummy_seq)

        sentences_data = [
            ["sentence"],
            ["Hello world, this is a test."],
            ["Another test sequence appears here."],
            ["No match in this sentence."]
        ]
        sentence_file = create_temp_csv(sentences_data)

        common_data = [
            ["common"],
            ["a"],
            ["in"],
            ["this"]
        ]
        common_file = create_temp_csv(common_data)

        try:
            engine = SearchEngine(
                seq_json_path=seq_json_path,
                preprocessed_flag=False,
                sentence_file=sentence_file,
                words_to_remove_file_path=common_file
            )
            self.assertTrue(len(engine.sentences) >= 1)
            self.assertTrue(all(hasattr(s, "word_list") for s in engine.sentences))
            expected_sequences = ["hello world", "test sequence"]
            self.assertEqual(engine.sequence_list, expected_sequences)
        finally:
            os.remove(sentence_file)
            os.remove(common_file)
            os.remove(seq_json_path)

    # Test static method find_sentences.
    def test_find_sentences(self):
        s1 = Sentence("Hello world, this is a test.", unwanted_words=[])
        s2 = Sentence("Another test sequence appears here.", unwanted_words=[])
        s3 = Sentence("No match in this sentence.", unwanted_words=[])
        s1.sequence_list = ["hello world", "world this", "this is", "is a", "a test"]
        s2.sequence_list = ["another test", "test sequence", "sequence appears", "appears here"]
        s3.sequence_list = ["no match", "match in", "in this", "this sentence"]
        sentences = [s1, s2, s3]
        result = SearchEngine.find_sentences("hello world", sentences)
        self.assertEqual(result, [s1])
        result = SearchEngine.find_sentences("test sequence", sentences)
        self.assertEqual(result, [s2])
        result = SearchEngine.find_sentences("not found", sentences)
        self.assertEqual(result, [])

    # Test build_dict produces expected JSON structure.
    def test_build_dict(self):
        s1 = Sentence("a b a", unwanted_words=[])
        s2 = Sentence("b c", unwanted_words=[])
        dummy_preprocessed = {
            "Question 1": {
                "Processed Sentences": [s1, s2]
            }
        }
        # Provide dummy sequences JSON with one key only.
        dummy_seq = {"keys": [["a", "b", "a"]]}
        import json_manager
        orig_load = json_manager.load_json_file
        json_manager.load_json_file = lambda path: dummy_preprocessed if "preprocessed" in path else dummy_seq
        try:
            engine = SearchEngine(
                seq_json_path=create_temp_json(dummy_seq),
                preprocessed_flag=True,
                preprocessed_json_file_path="dummy_preprocessed.json"
            )
            json_str = engine.build_dict()
            result = json.loads(json_str)
            self.assertIn("Question 4", result)
            q4 = result["Question 4"]
            self.assertIn("K-Seq Matches", q4)
            final_list = q4["K-Seq Matches"]
            self.assertEqual(len(final_list), 1)
            key, seq_list = final_list[0]
            self.assertEqual(key, "a b a")
            expected_seq_list = [s1.word_list]
            self.assertEqual(seq_list, expected_seq_list)
        finally:
            json_manager.load_json_file = orig_load


if __name__ == '__main__':
    unittest.main()
