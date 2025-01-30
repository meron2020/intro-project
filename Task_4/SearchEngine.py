from operator import index

from json_manager import *
from Task_1.Processor import Processor


class SearchEngine:
    def __init__(self, seq_json_path, preprocessed_flag, sentence_file=None, words_to_remove_file_path=None,
                 preprocessed_json=None):
        self.sentence_list = []
        self.sequences_lists = load_json_file(seq_json_path)["keys"]
        self.sequence_list = []
        for sequence_list in self.sequences_lists:
            sequence = ""
            for i in range(len(sequence_list)):
                sequence += sequence_list[i]
                if i != len(sequence_list) - 1:
                    sequence += " "
            self.sequence_list.append(sequence)


        if preprocessed_flag:
            self.sentence_list = preprocessed_json["Processed Sentences"]
        else:
            self.sentences = Processor.read_csv_file(sentence_file)
            words_to_remove = Processor.read_csv_file(words_to_remove_file_path)
            Processor.clean_sentences(self.sentences, words_to_remove)

    # Iterates over each sequence, and iterates over each sentence and checks if it is in that sentence,
    # If so, adds it to the list of sentences the sequence is in.
    def build_dict(self):
        #search_engine_dictionary = {}
        search_engine_list = []
        search_engine_dict = {}
        for sequence in sorted(self.sequence_list):
            sentences = self.find_sentences(sequence, self.sentences)
            if sentences and sequence not in search_engine_dict.keys():
                cleaned_sentences = []
                for sentence in sentences:
                    cleaned_sentences.append(sentence.word_list)
                search_engine_dict[sequence] = sorted(cleaned_sentences)

        for sequence in search_engine_dict.keys():
            search_engine_list.append([sequence, search_engine_dict[sequence]])
        return {"Question 4" :{"K-Seq Matches": search_engine_list}}

    @staticmethod
    def find_sentences(seq, sentences):
        sentence_list = []
        for sentence in sentences:
            if seq in sentence.sequence_list:
                sentence_list.append(sentence)
        return sentence_list
