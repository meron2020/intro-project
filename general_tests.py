import unittest

import deepdiff

import json_manager
from Task_1.Processor import Processor
from Task_2.SequenceCounter import SequenceCounter
from Task_3.PersonCounter import PersonCounter
from Task_4.SearchEngine import SearchEngine
from Task_5.ContextFinder import ContextFinder
from Task_6.DirectNeighborsFinder import DirectNeighborsFinder
from Task_7.IndirectConnectionFinder import IndirectConnectionFinder


class TestData(unittest.TestCase):
    def test_task_1(self):
        dictionaries = []
        for i in range(3):
            sentences = Processor.read_csv_file("C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q1_examples\\example_{}\\sentences_small_{}.csv".format(i+1, i+1))
            names = Processor.read_csv_file("C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q1_examples\\example_{}\\people_small_{}.csv".format(i+1, i+1))
            common_words = Processor.read_csv_file("C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\REMOVEWORDS.csv")

            Processor.clean(sentences, common_words)
            Processor.clean(names, common_words)
            Processor.remove_empty_sentences(sentences)
            Processor.remove_duplicate_names(names)
            example_dict = json_manager.load_json_file(
                "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q1_examples\\example_{}\\Q1_result{}.json".format(i+1, i+1))

            diff = deepdiff.DeepDiff(Processor.output_to_json(sentences, names), example_dict)
            dictionaries.append(diff)
        assert dictionaries == [{}, {}, {}]


    def test_task_2(self):
        dictionaries = []
        for i in range(3):
            counter = SequenceCounter(False, i+3,
                                      sentence_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q2_examples\\example_{}\\sentences_small_{}.csv".format(i+1,i+1),
                                      words_to_remove_file_path="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\REMOVEWORDS.csv")

            example_dict = json_manager.load_json_file(
                "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q2_examples\\example_{}\\Q2_result{}.json".format(i+1,i+1))
            print(SequenceCounter.create_final_dictionary(i+3, counter.sentences))
            print(example_dict)
            diff = deepdiff.DeepDiff(SequenceCounter.create_final_dictionary(i+3, counter.sentences), example_dict)
            dictionaries.append(diff)
        assert dictionaries == [{}, {}, {}]


    def test_task_3(self):
        dictionaries = []
        for i in range(4):
            counter = PersonCounter(False,
                                    name_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q3_examples\\example_{}\\people_small_{}.csv".format(i+1, i+1),
                                    sentence_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q3_examples\\example_{}\\sentences_small_{}.csv".format(i+1, i+1),
                                    words_to_remove_file_path="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\REMOVEWORDS.csv")

            example_dict = json_manager.load_json_file(
                "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q3_examples\\example_{}\\Q3_result{}.json".format(i+1, i+1))
            print(counter.count_person_appearances())
            print(example_dict)
            diff = deepdiff.DeepDiff(counter.count_person_appearances(), example_dict)
            dictionaries.append(diff)

        assert dictionaries == [{}, {}, {}, {}]

    def test_task_4(self):
        dictionaries = []
        for i in range(4):
            engine = SearchEngine(
                "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q4_examples\\example_{}\\kseq_query_keys_{}.json".format(i+1, i+1),
                False,
                sentence_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q4_examples\\example_{}\\sentences_small_{}.csv".format(i+1, i+1),
                words_to_remove_file_path="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\REMOVEWORDS.csv")

            example_dict = json_manager.load_json_file(
                "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q4_examples\\example_{}\\Q4_result{}.json".format(i+1, i+1))
            print(engine.build_dict())
            print(example_dict)
            diff = deepdiff.DeepDiff(engine.build_dict(), example_dict)
            print(diff)
            dictionaries.append(diff)
        assert dictionaries == [{}, {}, {}, {}]

    def test_task_5(self):
        dictionaries = []
        for i in range(4):
            counter = ContextFinder(
                preprocessed_flag=False,
                name_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q5_examples\\example_{}\\people_small_{}.csv".format(
                    i + 1, i + 1),
                sentence_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q5_examples\\example_{}\\sentences_small_{}.csv".format(
                    i + 1, i + 1),
                words_to_remove_file_path="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\REMOVEWORDS.csv")

            example_dict = json_manager.load_json_file(
                "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q5_examples\\example_{}\\Q5_result{}.json".format(
                    i + 1, i + 1))
            # print(counter.find_all_contexts(3))
            # print(example_dict)
            diff = deepdiff.DeepDiff(counter.find_all_contexts(i + 3), example_dict)
            dictionaries.append(diff)
        assert dictionaries == [{}, {}, {}, {}]

    def test_task_6(self):
        dictionaries = []
        options = [[4,4], [3,2], [5,2], [5,1]]
        result_options = [1,2,2,2]
        example_options = ["example", "exmaple", "exmaple", "exmaple"]
        for i in range(4):
            counter = DirectNeighborsFinder(
                preprocessed_flag=False, window_size=options[i][0], threshold=options[i][1],
                name_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q6_examples\\{}_{}\\people_small_{}.csv".format(example_options[i],i+1, i+1),
                sentence_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q6_examples\\{}_{}\\sentences_small_{}.csv".format(example_options[i],i+1, i+1),
                words_to_remove_file_path="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\REMOVEWORDS.csv")

            example_dict = json_manager.load_json_file(
                "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q6_examples\\{}_{}\\Q6_result{}_w{}_t{}.json".format(example_options[i], i+1, result_options[i],options[i][0], options[i][1],))
            # print(counter.find_all_contexts(3))
            # print(example_dict)
            counter.find_connections()

            diff = deepdiff.DeepDiff(counter.return_connections(), example_dict)
            dictionaries.append(diff)
        assert dictionaries == [{}, {}, {}, {}]

    def test_task_7(self):
        dictionaries = []
        options = [[5,2], [3,2], [5,1], [5,2]]
        result_options = [1,2,2,2]
        example_options = ["example", "exmaple", "exmaple", "exmaple"]
        for i in range(4):
            counter = IndirectConnectionFinder(
                maximal_distance= 1000,
                people_connections_path="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q7_examples\\example_1\\people_connections_1.json",
                preprocessed_flag=False, window_size=options[i][0], threshold=options[i][1],
                name_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q7_examples\\{}_{}\\people_small_{}.csv".format(example_options[i],i+1, i+1),
                sentence_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q7_examples\\{}_{}\\sentences_small_{}.csv".format(example_options[i],i+1, i+1),
                words_to_remove_file_path="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\REMOVEWORDS.csv")

            example_dict = json_manager.load_json_file(
                "C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q7_examples\\{}_{}\\Q7_result{}_w{}_t{}.json".format(example_options[i], i+1, i+1,options[i][0], options[i][1],))
            # print(counter.find_all_contexts(3))
            # print(example_dict)

            diff = deepdiff.DeepDiff(counter.find_indirect_connections(), example_dict)
            dictionaries.append(diff)
            print(diff)
        assert dictionaries == [{}, {}, {}, {}]

if __name__ == '__main__':
    unittest.main()
