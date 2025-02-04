import unittest
import sys
import json
import os
from unittest.mock import patch
from io import StringIO
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import run_program


# Define full paths
SENTENCES_FILE = "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\SENTENCES.csv"
NAMES_FILE = "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\NAMES.csv"
REMOVE_WORDS_FILE = "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\REMOVEWORDS.csv"
PREPROCESSED_JSON = "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\Preprocessed.json"


class TestMainExecution(unittest.TestCase):

    def run_test(self, test_args, expected_json_file):
        """Runs main.py with given system arguments and compares output to expected JSON."""
        expected_output = json.load(open(expected_json_file, "r"))  # Load expected output

        with patch.object(sys, "argv", test_args), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            run_program()
            actual_output = json.loads(mock_stdout.getvalue().strip())  # Convert output to JSON
            self.assertEqual(actual_output, expected_output)  # Compare expected vs actual output

    def test_task_1(self):
        """Test task 1 through main.py execution."""
        for i in range(3):
            sentences = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q1_examples\\example_{i + 1}\\sentences_small_{i + 1}.csv"
            names = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q1_examples\\example_{i + 1}\\people_small_{i + 1}.csv"
            expected_json = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q1_examples\\example_{i + 1}\\Q1_result{i + 1}.json"
            self.run_test(["main.py", "-t", "1", "-s", sentences, names, "-r", REMOVE_WORDS_FILE], expected_json)

    def test_task_2(self):
        """Test task 2 through main.py execution."""
        for i in range(3):
            sentences = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q2_examples\\example_{i + 1}\\sentences_small_{i + 1}.csv"
            expected_json = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q2_examples\\example_{i + 1}\\Q2_result{i + 1}.json"
            self.run_test(["main.py", "-t", "2", "-s", sentences, "-r", REMOVE_WORDS_FILE, "--maxk", str(i + 3)],
                          expected_json)

    def test_task_3(self):
        """Test task 3 through main.py execution."""
        for i in range(4):
            sentences = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q3_examples\\example_{i + 1}\\sentences_small_{i + 1}.csv"
            names = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q3_examples\\example_{i + 1}\\people_small_{i + 1}.csv"
            expected_json = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q3_examples\\example_{i + 1}\\Q3_result{i + 1}.json"
            self.run_test(["main.py", "-t", "3", "-s", sentences, names, "-r", REMOVE_WORDS_FILE], expected_json)

    def test_task_4(self):
        """Test task 4 through main.py execution."""
        for i in range(4):
            sentences = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q4_examples\\example_{i + 1}\\sentences_small_{i + 1}.csv"
            query = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q4_examples\\example_{i + 1}\\kseq_query_keys_{i + 1}.json"
            expected_json = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q4_examples\\example_{i + 1}\\Q4_result{i + 1}.json"
            self.run_test(["main.py", "-t", "4", "-s", sentences, "-r", REMOVE_WORDS_FILE, "--qsek_query_path", query],
                          expected_json)

    def test_task_5(self):
        """Test task 5 through main.py execution."""
        for i in range(4):
            sentences = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q5_examples\\example_{i + 1}\\sentences_small_{i + 1}.csv"
            names = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q5_examples\\example_{i + 1}\\people_small_{i + 1}.csv"
            expected_json = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q5_examples\\example_{i + 1}\\Q5_result{i + 1}.json"
            self.run_test(["main.py", "-t", "5", "-s", sentences, names, "-r", REMOVE_WORDS_FILE, "--maxk", str(i + 3)],
                          expected_json)

    def test_task_6(self):
        """Test task 6 through main.py execution."""
        result_options = [1, 2, 2, 2]
        options = [[4, 4], [3, 2], [5, 2], [5, 1]]
        examples = ["example", "exmaple", "exmaple", "exmaple"]
        for i in range(4):
            sentences = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q6_examples\\{examples[i]}_{i + 1}\\sentences_small_{i + 1}.csv"
            names = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q6_examples\\{examples[i]}_{i + 1}\\people_small_{i + 1}.csv"
            expected_json = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q6_examples\\{examples[i]}_{i + 1}\\Q6_result{result_options[i]}_w{options[i][0]}_t{options[i][1]}.json"
            self.run_test(["main.py", "-t", "6", "-s", sentences, names, "-r", REMOVE_WORDS_FILE,
                           "--windowsize", str(options[i][0]), "--threshold", str(options[i][1])], expected_json)

    def test_task_7(self):
        """Test task 7 through main.py execution."""
        examples = ["example", "exmaple", "exmaple", "exmaple"]
        options = [[5, 2], [3, 2], [5, 1], [5, 2]]
        for i in range(4):
            sentences = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q7_examples\\{examples[i]}_{i + 1}\\sentences_small_{i + 1}.csv"
            names = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q7_examples\\{examples[i]}_{i + 1}\\people_small_{i + 1}.csv"
            pairs = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q7_examples\\{examples[i]}_{i + 1}\\people_connections_{i + 1}.json"
            expected_json = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q7_examples\\{examples[i]}_{i + 1}\\Q7_result{i+1}_w{options[i][0]}_t{options[i][1]}.json"
            self.run_test(["main.py", "-t", "7", "-s", sentences, names, "-r", REMOVE_WORDS_FILE,
                           "--pairs", pairs, "--maximal_distance", "1000",
                           "--windowsize", str(options[i][0]), "--threshold", str(options[i][1])], expected_json)

    def test_task_8(self):
        """Test task 8 through main.py execution."""
        options = [[3, 2, 2], [3, 2, 3], [3, 2, 8]]
        examples = ["example", "exmaple", "exmaple", "exmaple"]

        for i in range(3):
            sentences = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q8_examples\\{examples[i]}_{i + 1}\\sentences_small_{i + 1}.csv"
            names = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q8_examples\\{examples[i]}_{i + 1}\\people_small_{i + 1}.csv"
            pairs = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q8_examples\\{examples[i]}_{i + 1}\\people_connections_{i + 1}.json"
            expected_json = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q8_examples\\{examples[i]}_{i + 1}\\Q8_example_{i+1}_w_{options[i][0]}_threshold_{options[i][1]}_fixed_length_{options[i][2]}.json"
            self.run_test(["main.py", "-t", "8", "-s", sentences, names, "-r", REMOVE_WORDS_FILE,
                           "--pairs", pairs, "--fixed_length", str(options[i][2]), "--windowsize", str(options[i][0]), "--threshold", str(options[i][1])], expected_json)

    def test_task_9(self):
        """Test task 9 through main.py execution."""
        thresholds = [1, 3, 6]
        examples = ["example", "exmaple", "exmaple"]

        for i in range(3):
            sentences = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q9_examples\\{examples[i]}_{i + 1}\\sentences_small_{i + 1}.csv"
            expected_json = f"C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q9_examples\\{examples[i]}_{i + 1}\\Q9_result{i + 1}.json"
            self.run_test(["main.py", "-t", "9", "-s", sentences, "-r", REMOVE_WORDS_FILE,
                           "--threshold", str(thresholds[i])], expected_json)

    def test_invalid_task(self):
        """Test invalid task number."""
        args = ["main.py", "-t", "999", "-s", SENTENCES_FILE, NAMES_FILE, "-r", REMOVE_WORDS_FILE]
        with patch.object(sys, "argv", args), patch("sys.stdout", new_callable=StringIO) as stdout:
            with self.assertRaises(SystemExit) as cm:
                run_program()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("invalid input", stdout.getvalue().strip())

    def test_missing_argument(self):
        """Test missing -s argument."""
        args = ["main.py", "-t", "1", "-r", REMOVE_WORDS_FILE]
        with patch.object(sys, "argv", args), patch("sys.stdout", new_callable=StringIO) as stdout:
            with self.assertRaises(SystemExit) as cm:
                run_program()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn("invalid input", stdout.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
