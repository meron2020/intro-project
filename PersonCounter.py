import json

import json_manager
from Processor import Processor


class PersonCounter:
    def __init__(self, preprocessed_flag, name_file=None, sentence_file=None, words_to_remove_file_path=None, preprocessed_json_file_path=None):
        if preprocessed_flag:
            # Unpacks the sentences and people from the json that is in the same format as task 1
            preprocessed_json = json_manager.load_json_file(preprocessed_json_file_path)
            self.sentences = preprocessed_json["Question 1"]["Processed Sentences"]
            self.names = preprocessed_json["Question 1"]["Processed Names"]
        else:
            # Executes the preprocessing cleaning procedure and sets the variables needed (sentences and persons)
            self.sentences = Processor.read_csv_file(sentence_file)
            self.persons = Processor.read_csv_file(name_file)
            words_to_remove = Processor.read_csv_file(words_to_remove_file_path)
            Processor.clean_sentences(self.sentences, words_to_remove)
            for person in self.persons:
                person.clean(words_to_remove)  # Cleans each person's name by removing unwanted words.

    @staticmethod
    # Turns seq_dict to key-value tuples
    def turn_dict_to_list(seq_dict):
        list_of_lists = []
        for seq in sorted(seq_dict.keys()):  # Ensures sorted order of keys before converting to list.
            list_of_lists.append([seq, seq_dict[seq]])

        return list_of_lists

    # Iterates over the sentences and counts the appearance of each person and returns dictionary name to number
    def count_person_appearances(self):
        person_mention_dict = {}
        for person in self.persons:
            mention_counter = 0
            for sentence in self.sentences:
                mention_counter += sentence.check_for_names(person)  # Counts occurrences of the person's name in sentences.
            if mention_counter > 0:  # Only store persons who appear at least once.
                person_mention_dict[person.real_name.cleaned_data] = mention_counter

        return json.dumps({"Question 3": {"Name Mentions": PersonCounter.turn_dict_to_list(person_mention_dict)}})  # Converts dict to list format.
