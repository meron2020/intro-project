import json

import json_manager
from Person import Person
from Processor import Processor
from SequenceCounter import SequenceCounter


class ContextFinder:
    def __init__(self, preprocessed_flag, name_file=None, sentence_file=None, words_to_remove_file_path=None,
                 preprocessed_json_file_path=None):
        if preprocessed_flag:
            # Unpacks the sentences and people from the json that is in the same format as task 1
            preprocessed_json = json_manager.load_json_file(preprocessed_json_file_path)
            self.sentences = preprocessed_json["Question 1"]["Processed Sentences"]
            self.persons = preprocessed_json["Question 1"]["Persons"]
        else:
            # Executes the preprocessing cleaning procedure and sets the variables needed (sentences and persons)
            words_to_remove = Processor.read_csv_file(words_to_remove_file_path)
            self.sentences = Processor.read_csv_file(sentence_file, words_to_remove)
            Processor.clean_sentences(self.sentences, words_to_remove)
            self.persons = Processor.read_csv_file(name_file)
            for person in self.persons:
                person.clean(words_to_remove)

    # Function returns all sequences related to a person.
    def find_context(self, person: Person, max_length: int) -> list:
        relevant_sequences = []
        sentences = []
        # Find all sentences that contain the person
        for sentence in self.sentences:
            if sentence.check_if_person_in_sentence(person):
                sentences.append(sentence)

        # Add all unique sequences to the relevant_sequences list that are at most of length max_length
        for i in range(1, max_length + 1):
            sequence_list = SequenceCounter.create_sequence_list(i, sentences)
            for sequence in sequence_list:
                if sequence.split(" ") not in relevant_sequences:
                    relevant_sequences.append(sequence.split(" "))

        # Sorts the relevant sequences lexicographically
        return sorted(relevant_sequences)

    # Function returns required kseq list for each person.
    def find_all_contexts(self, max_length:int) -> str:
        context_dict = {}
        # Iterates over each person and finds all their relevant sequences.
        for person in self.persons:
            relevant_sequences = self.find_context(person, max_length)
            context_dict[person.real_name] = relevant_sequences

        # Creates the format required and sorts the dictionary by keys.
        context_list = []
        for name in sorted(context_dict.keys(), key=lambda name: name.cleaned_data):
            if context_dict[name]:
                context_list.append([name.cleaned_data, context_dict[name]])
        return json.dumps({"Question 5": {"Person Contexts and K-Seqs": context_list}})
