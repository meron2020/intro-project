import unittest

import deepdiff

import json_manager
from Task_6.DirectNeighborsFinder import DirectNeighborsFinder


class TestData(unittest.TestCase):

    def test_output_to_example(self):
        counter = DirectNeighborsFinder(
            preprocessed_flag=False, window_size=5, threshold=1,
            name_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q6_examples\\exmaple_4\\people_small_4.csv",
            sentence_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q6_examples\\exmaple_4\\sentences_small_4.csv",
            words_to_remove_file_path="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\REMOVEWORDS.csv")

        example_dict = json_manager.load_json_file(
            "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q6_examples\\exmaple_4\\Q6_result2_w5_t1.json")
        #print(counter.find_all_contexts(3))
        #print(example_dict)
        counter.find_connections()
        print(counter.return_connections())
        print("\n")
        print(example_dict)

        print(len(example_dict["Question 6"]["Pair Matches"]))
        print(len(counter.return_connections()["Question 6"]["Pair Matches"]))

        for pair in counter.return_connections()["Question 6"]["Pair Matches"]:
            if pair not in example_dict["Question 6"]["Pair Matches"]:
                print(pair)

        diff = deepdiff.DeepDiff(counter.return_connections(), example_dict)
        print(diff)
        assert diff == {}

