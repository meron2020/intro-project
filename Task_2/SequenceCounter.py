import json

from Sentence import Sentence
from Task_1.Processor import Processor


class SequenceCounter:

    def __init__(self, preprocessed_flag, max_length, sentence_file=None, words_to_remove_file_path=None, preprocessed_json=None):
        self.sentence_list = []
        if preprocessed_flag:
            self.sentence_list = preprocessed_json["Processed Sentences"]
        else:
            self.sentences = Processor.read_csv_file(sentence_file)
            words_to_remove = Processor.read_csv_file(words_to_remove_file_path)
            Processor.clean_sentences(self.sentences, words_to_remove)

    @staticmethod
    def create_seq_list_for_sentence(seq_length, sentence):
        sequence_list = []
        sentence_seq_list = sentence.create_sequence_list(seq_length)
        for sequence in sentence_seq_list:
            sequence_list.append(sequence)
        return sequence_list

    # Function returns list of all the seq_length sequences in all the sentences.
    # Iterates over each sentence object and runs the sequence counter function
    @staticmethod
    def create_sequence_list(seq_length, sentences):
        sequence_list = []
        for sentence in sentences:
            sequence_list += SequenceCounter.create_seq_list_for_sentence(seq_length, sentence)
        return sequence_list

    @staticmethod
    # Returns a dictionary with numbering of each sequence.
    # The keys should be sorted by alphabetical order.
    def count_each_sequence(sequence_list):
        sequence_to_num = {}
        for sequence in sequence_list:
            sequence_to_num[sequence] = sequence_list.count(sequence)

        return sequence_to_num

    @staticmethod
    # Turns seq_dict to key-value tuples
    def turn_dict_to_list(seq_dict):
        list_of_lists = []
        for seq in sorted(seq_dict.keys()):
            list_of_lists.append([seq, seq_dict[seq]])

        return list_of_lists

    # {
    #     "Question 2": {
    #         "3-Seq Counts": [
    #             ["1_seq", [["away", 1], ["caught", 1], ["flew", 1], ["harry", 1], ["hermione", 1], ["snitch", 3]]],
    #             ["2_seq", [["caught snitch", 1], ["flew away", 1], ["harry caught", 1], ["hermione snitch", 1],
    #                        ["snitch flew", 1]]],
    #             ["3_seq", [["harry caught snitch", 1], ["snitch flew away", 1]]]
    #         ]
    #     }
    # }
    @staticmethod
    # Function iterates from 0 to max_sequences and adds all dictionaries together
    def create_final_dictionary(max_length, sentences):
        final_dict = {}
        for i in range(1, max_length + 1):
            seq_list = SequenceCounter.count_each_sequence(SequenceCounter.create_sequence_list(i, sentences))
            final_dict[str(i) + "_seq"] = SequenceCounter.turn_dict_to_list(seq_list)

        return {"Question 2" :{str(max_length) + "-Seq Counts": SequenceCounter.turn_dict_to_list(final_dict)}}


