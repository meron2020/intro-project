import Data


class Sentence(Data.Data):
    def __init__(self, data, unwanted_words):
        super().__init__(data)
        self.clean(unwanted_words)

    # Function returns true if cleaned_sentence is empty string
    def sentence_empty(self):
        return self.cleaned_data == ""

    def check_for_names(self, person):
        counter = 0
        for word in person.real_name.word_list:
            if word in self.word_list:
                counter += self.word_list.count(word)
        for nickname in person.nicknames:
            if nickname.cleaned_data != "":
                if nickname.cleaned_data in self.cleaned_data:
                    counter += self.cleaned_data.count(nickname.cleaned_data)

        return counter

    def check_if_person_in_sentence(self, person):
        for word in person.real_name.word_list:
            if word in self.word_list:
                return True
        for nickname in person.nicknames:
            if nickname.cleaned_data != "":
                if nickname.cleaned_data in self.cleaned_data:
                    return True
        return False
