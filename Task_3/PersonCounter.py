from Task_1.Processor import Processor


class PersonCounter:
    def __init__(self, preprocessed_flag, name_file = None,sentence_file = None, words_to_remove_file_path = None, preprocessed_json = None):
        self.sentence_list = []
        if preprocessed_flag:
            self.sentence_list = preprocessed_json["Processed Sentences"]
            self.names = preprocessed_json["Processed Names"]
        else:
            self.sentences = Processor.read_csv_file(sentence_file)
            self.persons = Processor.read_csv_file(name_file)
            words_to_remove = Processor.read_csv_file(words_to_remove_file_path)
            Processor.clean_sentences(self.sentences, words_to_remove)
            for person in self.persons:
                person.clean(words_to_remove)

    @staticmethod
    # Turns seq_dict to key-value tuples
    def turn_dict_to_list(seq_dict):
        list_of_lists = []
        for seq in sorted(seq_dict.keys()):
            list_of_lists.append([seq, seq_dict[seq]])

        return list_of_lists

    # Iterates over the sentences and counts the appearance of each person and returns dictionary name to number
    def count_person_appearances(self):
        person_mention_dict = {}
        for person in self.persons:
            mention_counter = 0
            for sentence in self.sentences:
                mention_counter += sentence.check_for_names(person)
            if mention_counter > 0:
                person_mention_dict[person.real_name.cleaned_data] = mention_counter



        return {"Question 3": {"Name Mentions": PersonCounter.turn_dict_to_list(person_mention_dict)}}
