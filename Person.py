import Sentence
from Data import Data

class Person:
    def __init__(self, name, nicknames):
        self.real_name = Data(name)
        self.nicknames = [Data(nickname) for nickname in nicknames.split(',')]
        self.connections = []
        self.sequence_list = self.real_name.sequence_list
        for nickname in self.nicknames:
         self.sequence_list += nickname.sequence_list

    # Function returns the list of cleaned nicknames
    def return_nickname_list(self):
        return [nickname.cleaned_data for nickname in self.nicknames]

    # Function cleans the real name and the nicknames of the person
    def clean(self, unwanted_words):
        self.real_name.clean(unwanted_words)
        for nickname in self.nicknames:
            nickname.clean(unwanted_words)


    # Function returns True if the nickname belongs to this person
    def nickname_is_person(self, nickname):
        pass

    # Function returns number of times person is mentioned in sentence
    # Not count same person twice
    def check_person_in_sentence(self, sentence) -> Sentence:
        if sentence.count_sequence_in_sequence_list(self.real_name):
            return sentence

    # Iterates over sentences and returns a list of sentence_windows person exists in
    def find_persons_sentence_windows(self, person, sentence_windows):
        pass

    # Iterates over all persons, checks how many windows together in.
    # If >= than needed amount, add edge. Make sure to add edge back.
    # Check if edge already exists to not add twice. And make sure to check self.
    def find_connections(self):
        pass




