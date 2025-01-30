from Task_1.Processor import Processor
from Task_2.SequenceCounter import SequenceCounter
from Task_4.SearchEngine import SearchEngine


class ContextFinder:
    def __init__(self, preprocessed_flag, name_file=None, sentence_file=None, words_to_remove_file_path=None,
                 preprocessed_json=None):
        self.sentence_list = []
        if preprocessed_flag:
            self.sentences = preprocessed_json["Processed Sentences"]
        else:
            words_to_remove = Processor.read_csv_file(words_to_remove_file_path)
            self.sentences = Processor.read_csv_file(sentence_file, words_to_remove)
            Processor.clean_sentences(self.sentences, words_to_remove)
            self.persons = Processor.read_csv_file(name_file)
            for person in self.persons:
                person.clean(words_to_remove)

    def find_context(self, person, max_length):
        relevant_sequences = []
        sentences = []
        for sentence in self.sentences:
            if sentence.check_if_person_in_sentence(person):
                sentences.append(sentence)
        #sentences = SearchEngine.find_sentences(person.real_name.cleaned_data, self.sentences)
        # for nickname in person.nicknames:
        #     sentences += SearchEngine.find_sentences(nickname.cleaned_data, self.sentences)
        for i in range(1, max_length + 1):
            sequence_list = SequenceCounter.create_sequence_list(i, sentences)
            for sequence in sequence_list:
                if sequence.split(" ") not in relevant_sequences:
                    relevant_sequences.append(sequence.split(" "))
        return sorted(relevant_sequences)

    def find_all_contexts(self, max_length):
        context_dict = {}
        for person in self.persons:
            relevant_sequences = self.find_context(person, max_length)
            context_dict[person.real_name] = relevant_sequences

        context_list = []
        for name in sorted(context_dict.keys(), key=lambda name: name.cleaned_data):
            if context_dict[name]:
                context_list.append([name.cleaned_data, context_dict[name]])
        return {"Question 5": {"Person Contexts and K-Seqs": context_list}}
