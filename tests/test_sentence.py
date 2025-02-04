import os
import sys
import tempfile
import unittest
import csv
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Sentence import Sentence
from Person import Person

# Helper function to create temporary CSV files
def create_temp_csv(rows):
    # Create a temporary CSV file; first row is the header.
    temp = tempfile.NamedTemporaryFile(mode="w+", newline="", delete=False, encoding="utf-8")
    writer = csv.writer(temp)
    for row in rows:
        writer.writerow(row)
    temp.close()
    return temp.name

# Test that sentence_empty works correctly
class TestSentence(unittest.TestCase):

    # Test that sentence_empty returns True for an empty sentence and False for a non-empty sentence.
    def test_sentence_empty(self):
        s_empty = Sentence("   ,,,   ", unwanted_words=[])
        self.assertTrue(s_empty.sentence_empty())
        s_nonempty = Sentence("Hello world!", unwanted_words=[])
        self.assertFalse(s_nonempty.sentence_empty())

    # Test that check_if_person_in_sentence returns True when the person's name is present.
    def test_check_if_person_in_sentence(self):
        p = Person("Alice", "Ally")
        p.clean([])  # Clean person so names become lowercase
        s1 = Sentence("Alice went to the market", unwanted_words=[])
        self.assertTrue(s1.check_if_person_in_sentence(p))
        s2 = Sentence("Bob is here", unwanted_words=[])
        self.assertFalse(s2.check_if_person_in_sentence(p))

    # Test that check_for_names correctly counts occurrences of a person's name and nickname.
    def test_check_for_names(self):
        p = Person("Alice", "Ally")
        p.clean([])
        s = Sentence("Alice and Ally are here. Alice is present.", unwanted_words=[])
        self.assertEqual(s.check_for_names(p), 3)
        s2 = Sentence("Bob is here", unwanted_words=[])
        self.assertEqual(s2.check_for_names(p), 0)

    # Test that sentence_is_similar returns the correct boolean based on shared common words.
    def test_sentence_is_similar(self):
        s1 = Sentence("The quick brown fox", unwanted_words=["the"])
        s2 = Sentence("A quick brown dog", unwanted_words=["a"])
        self.assertTrue(s1.sentence_is_similar(s2, threshold=2))
        self.assertFalse(s1.sentence_is_similar(s2, threshold=3))
        s3 = Sentence("Jumped over the lazy dog", unwanted_words=["the"])
        self.assertFalse(s1.sentence_is_similar(s3, threshold=1))

if __name__ == '__main__':
    unittest.main()
