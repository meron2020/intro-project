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



