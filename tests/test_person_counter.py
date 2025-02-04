import csv
import json
import os
import sys
import tempfile
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Person import Person
from Sentence import Sentence
from Processor import Processor
from PersonCounter import PersonCounter

# --- Helper Methods for Creating Temporary CSV Files ---

def create_temp_csv(data_rows):
    # Creates a temporary CSV file with the given rows; first row is the header.
    temp_file = tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False, encoding="utf-8")
    writer = csv.writer(temp_file)
    for row in data_rows:
        writer.writerow(row)
    temp_file.close()
    return temp_file.name

# --- Test Suite for PersonCounter ---

class TestPersonCounter(unittest.TestCase):

    # Test that turn_dict_to_list converts a dictionary to a sorted list of [key, value] pairs.
    def test_turn_dict_to_list(self):
        input_dict = {"bob": 3, "alice": 5, "charlie": 2}
        expected = [["alice", 5], ["bob", 3], ["charlie", 2]]
        result = PersonCounter.turn_dict_to_list(input_dict)
        self.assertEqual(result, expected)

    # Test __init__ with preprocessed_flag True: loads sentences and names from JSON.
    def test_init_preprocessed_true(self):
        # Create dummy Sentence objects.
        s1 = Sentence("Dummy sentence one.", unwanted_words=[])
        s2 = Sentence("Dummy sentence two.", unwanted_words=[])
        # Dummy names in processed structure: each name as [real_name_word_list, list of nickname word lists].
        dummy_names = [
            [["alice"], [["ally"]]],
            [["bob"], [["bobby"]]]
        ]
        dummy_json = {
            "Question 1": {
                "Processed Sentences": [s1, s2],
                "Processed Names": dummy_names
            }
        }
        # Monkey-patch json_manager.load_json_file to return our dummy JSON.
        import json_manager
        orig_load = json_manager.load_json_file
        json_manager.load_json_file = lambda fp: dummy_json
        try:
            pc = PersonCounter(
                preprocessed_flag=True,
                preprocessed_json_file_path="dummy.json"
            )
            self.assertEqual(pc.sentences, [s1, s2])
            self.assertEqual(pc.names, dummy_names)
        finally:
            json_manager.load_json_file = orig_load

    # Test __init__ with preprocessed_flag False using temporary CSV files.
    def test_init_preprocessed_false_with_temp_files(self):
        # Prepare CSV data for sentences.
        sentences_data = [
            ["sentence"],
            ["This is the first sentence."],
            ["And here is the second sentence!"]
        ]
        # Prepare CSV data for names.
        names_data = [
            ["Name"],
            ["Alice", "Ally"],
            ["Bob", "Bobby"]
        ]
        # Prepare CSV data for common words.
        common_data = [
            ["common"],
            ["is"],
            ["the"],
            ["and"]
        ]
        sentence_file = create_temp_csv(sentences_data)
        name_file = create_temp_csv(names_data)
        common_file = create_temp_csv(common_data)
        try:
            pc = PersonCounter(
                preprocessed_flag=False,
                sentence_file=sentence_file,
                name_file=name_file,
                words_to_remove_file_path=common_file
            )
            self.assertTrue(len(pc.sentences) >= 1)
            self.assertTrue(all(isinstance(s, Sentence) for s in pc.sentences))
            self.assertTrue(len(pc.persons) >= 1)
            self.assertTrue(all(isinstance(p, Person) for p in pc.persons))
        finally:
            os.remove(sentence_file)
            os.remove(name_file)
            os.remove(common_file)

    # Test count_person_appearances using temporary CSV files and overriding check_for_names.
    def test_count_person_appearances_with_temp_files(self):
        # Prepare CSV data for sentences.
        sentences_data = [
            ["sentence"],
            ["Dummy sentence for counting."]
        ]
        # Prepare CSV data for names.
        names_data = [
            ["Name"],
            ["Alice", "Ally"],
            ["Bob", "Bobby"]
        ]
        # Prepare CSV data for common words.
        common_data = [
            ["common"]
        ]
        sentence_file = create_temp_csv(sentences_data)
        name_file = create_temp_csv(names_data)
        common_file = create_temp_csv(common_data)
        try:
            pc = PersonCounter(
                preprocessed_flag=False,
                sentence_file=sentence_file,
                name_file=name_file,
                words_to_remove_file_path=common_file
            )
            # Clean persons so that cleaned_data is set.
            for person in pc.persons:
                person.clean([])
            # Override check_for_names: simulate "alice" mentioned 2 times, "bob" 0 times.
            for sentence in pc.sentences:
                sentence.check_for_names = lambda person: 2 if person.real_name.cleaned_data == "alice" else 0
            json_output = pc.count_person_appearances()
            output = json.loads(json_output)
            expected = {"Question 3": {"Name Mentions": [["alice", 2]]}}
            self.assertEqual(output, expected)
        finally:
            os.remove(sentence_file)
            os.remove(name_file)
            os.remove(common_file)

    # Test that persons with zero mentions are excluded.
    def test_count_person_appearances_excludes_zero_mentions(self):
        sentences_data = [
            ["sentence"],
            ["Dummy sentence for testing."]
        ]
        names_data = [
            ["Name"],
            ["Alice", "Ally"],
            ["Bob", "Bobby"],
            ["Charlie", "Chuck"]
        ]
        common_data = [
            ["common"]
        ]
        sentence_file = create_temp_csv(sentences_data)
        name_file = create_temp_csv(names_data)
        common_file = create_temp_csv(common_data)
        try:
            pc = PersonCounter(
                preprocessed_flag=False,
                sentence_file=sentence_file,
                name_file=name_file,
                words_to_remove_file_path=common_file
            )
            for person in pc.persons:
                person.clean([])
            # Override check_for_names:
            # "alice" appears 2 times, "charlie" 1 time, "bob" 0 times.
            for sentence in pc.sentences:
                sentence.check_for_names = lambda person: 2 if person.real_name.cleaned_data == "alice" \
                    else (1 if person.real_name.cleaned_data == "charlie" else 0)
            json_output = pc.count_person_appearances()
            output = json.loads(json_output)
            expected = {"Question 3": {"Name Mentions": [["alice", 2], ["charlie", 1]]}}
            self.assertEqual(output, expected)
        finally:
            os.remove(sentence_file)
            os.remove(name_file)
            os.remove(common_file)

if __name__ == '__main__':
    unittest.main()
