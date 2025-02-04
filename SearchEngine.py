import json_manager
from json_manager import *
from Processor import Processor


class SearchEngine:
    def __init__(self, seq_json_path, preprocessed_flag, sentence_file=None, words_to_remove_file_path=None,
                 preprocessed_json_file_path=None):
        # Loads the sequences to be searched for from the JSON file.
        self.sequences_lists = load_json_file(seq_json_path)["keys"]
        self.sequence_list = []

        # Converts the list of sequences into space-separated strings.
        for sequence_list in self.sequences_lists:
            sequence = ""
            for i in range(len(sequence_list)):
                sequence += sequence_list[i]
                if i != len(sequence_list) - 1:
                    sequence += " "  # Adds spaces between words except for the last one.
            self.sequence_list.append(sequence)

        if preprocessed_flag:
            # Loads preprocessed sentences if available.
            preprocessed_json = json_manager.load_json_file(preprocessed_json_file_path)
            self.sentences = preprocessed_json["Question 1"]["Processed Sentences"]
        else:
            # Reads raw sentences and cleans them using the words to remove.
            self.sentences = Processor.read_csv_file(sentence_file)
            words_to_remove = Processor.read_csv_file(words_to_remove_file_path)
            Processor.clean_sentences(self.sentences, words_to_remove)

    # Iterates over each sequence and checks for occurrences in the sentences.
    # If a sequence appears in any sentence, it is added to the results.
    def build_dict(self):
        search_engine_list = []
        search_engine_dict = {}

        for sequence in sorted(self.sequence_list):  # Ensures sequences are processed in sorted order.
            sentences = self.find_sentences(sequence, self.sentences)  # Finds sentences containing the sequence.
            if sentences and sequence not in search_engine_dict.keys():
                cleaned_sentences = []
                for sentence in sentences:
                    cleaned_sentences.append(sentence.word_list)  # Converts sentence objects to word lists.
                search_engine_dict[sequence] = sorted(cleaned_sentences)  # Stores sorted matching sentences.

        for sequence in search_engine_dict.keys():
            search_engine_list.append([sequence, search_engine_dict[sequence]])  # Converts dictionary to list format.

        return json.dumps({"Question 4": {"K-Seq Matches": search_engine_list}})  # Returns results in required JSON format.

    @staticmethod
    # Finds all sentences that contain the given sequence.
    def find_sentences(seq, sentences):
        sentence_list = []
        for sentence in sentences:
            if seq in sentence.sequence_list:  # Checks if the sequence appears in the sentence.
                sentence_list.append(sentence)
        return sentence_list  # Returns the list of matching sentences.
