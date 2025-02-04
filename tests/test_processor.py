import csv
import json
import os
import sys
import tempfile
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Processor import Processor
from Person import Person
from Sentence import Sentence
from Data import Data

# --- Helper Functions ---

def create_temp_csv(header, rows):
    # Creates a temporary CSV file with the given header and rows.
    temp_file = tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False, encoding="utf-8")
    writer = csv.writer(temp_file)
    writer.writerow([header])
    for row in rows:
        writer.writerow(row)
    temp_file.close()
    return temp_file.name

# --- Test Suite for Processor ---

class TestProcessor(unittest.TestCase):

    # Test read_csv_file creates Sentence objects when header is "sentence"
    def test_read_csv_file_sentences(self):
        rows = [
            ["This is the first sentence."],
            ["And here is another sentence!"]
        ]
        file_name = create_temp_csv("sentence", rows)
        try:
            # Pass None for unwanted_words so that no words are removed.
            result = Processor.read_csv_file(file_name, unwanted_words=None)
            self.assertEqual(len(result), 2)
            for sent in result:
                self.assertIsInstance(sent, Sentence)
                self.assertIsNotNone(sent.word_list)
        finally:
            os.remove(file_name)

    # Test read_csv_file creates Person objects when header is "Name"
    def test_read_csv_file_names(self):
        rows = [
            ["Alice", "Ally,A"],
            ["Bob", "Bobby,Robert"]
        ]
        file_name = create_temp_csv("Name", rows)
        try:
            result = Processor.read_csv_file(file_name)
            self.assertEqual(len(result), 2)
            for person in result:
                self.assertIsInstance(person, Person)
                self.assertTrue(hasattr(person, "real_name"))
                self.assertTrue(isinstance(person.nicknames, list))
        finally:
            os.remove(file_name)

    # Test read_csv_file returns list of strings for common words files (header not "sentence" or "Name")
    def test_read_csv_file_common(self):
        rows = [
            ["the"],
            ["and"],
            ["a"]
        ]
        file_name = create_temp_csv("common", rows)
        try:
            result = Processor.read_csv_file(file_name)
            self.assertEqual(len(result), 3)
            for word in result:
                self.assertIsInstance(word, str)
        finally:
            os.remove(file_name)

    # Test that Processor.clean calls each object's clean method (Data cleaning)
    def test_clean_method(self):
        common_words = ["and", "the"]
        data_obj = Data("Hello, the world!")
        self.assertEqual(data_obj.sequence_list, [])
        Processor.clean([data_obj], common_words)
        # "Hello, the world!" -> "hello world" (assuming "the" is removed)
        self.assertEqual(data_obj.cleaned_data, "hello world")
        self.assertIsNotNone(data_obj.word_list)
        self.assertTrue(len(data_obj.sequence_list) > 0)

    # Test remove_duplicate_names returns only the first occurrence of a duplicate Person
    def test_remove_duplicate_names(self):
        person1 = Person("Alice", "Ally")
        person2 = Person("Alice", "Alicia")
        person1.clean([])
        person2.clean([])
        persons = [person1, person2]
        unique_persons = Processor.remove_duplicate_names(persons)
        self.assertEqual(len(unique_persons), 1)
        self.assertEqual(unique_persons[0].real_name.cleaned_data, person1.real_name.cleaned_data)

    # Test that remove_empty_sentences removes Sentence objects that are empty
    def test_remove_empty_sentences(self):
        non_empty = Sentence("This is a sentence.", unwanted_words=None)
        empty_sentence = Sentence(",,,", unwanted_words=None)
        empty_sentence.clean([])
        self.assertTrue(empty_sentence.sentence_empty())
        sentences = [non_empty, empty_sentence]
        Processor.remove_empty_sentences(sentences)
        self.assertEqual(len(sentences), 1)
        self.assertFalse(sentences[0].sentence_empty())

    # Test that clean_sentences cleans each Sentence and then removes empty ones
    def test_clean_sentences(self):
        common_words = ["a", "an", "the"]
        s1 = Sentence("The quick brown fox", unwanted_words=None)
        s2 = Sentence("a an the", unwanted_words=None)
        sentences = [s1, s2]
        Processor.clean_sentences(sentences, common_words)
        self.assertEqual(len(sentences), 1)
        self.assertFalse(sentences[0].sentence_empty())

    # Test that output_to_json returns JSON with the expected structure.
    def test_output_to_json(self):
        sentences_rows = [
            ["This is the first sentence."],
            ["Second sentence here."]
        ]
        sentences_file = create_temp_csv("sentence", sentences_rows)
        names_rows = [
            ["Alice", "Ally"],
            ["Bob", "Bobby"]
        ]
        names_file = create_temp_csv("Name", names_rows)
        common_rows = [
            ["is"],
            ["the"],
            ["here"]
        ]
        common_file = create_temp_csv("common", common_rows)
        try:
            json_str = Processor.output_to_json(sentences_file, names_file, common_file)
            output = json.loads(json_str)
            self.assertIn("Question 1", output)
            q1 = output["Question 1"]
            self.assertIn("Processed Sentences", q1)
            self.assertIn("Processed Names", q1)
            self.assertIsInstance(q1["Processed Sentences"], list)
            for name_item in q1["Processed Names"]:
                self.assertIsInstance(name_item, list)
                self.assertEqual(len(name_item), 2)
                self.assertIsInstance(name_item[0], list)
                self.assertIsInstance(name_item[1], list)
        finally:
            os.remove(sentences_file)
            os.remove(names_file)
            os.remove(common_file)

if __name__ == '__main__':
    unittest.main()
