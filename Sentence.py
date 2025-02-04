import Data


class Sentence(Data.Data):
    def __init__(self, data, unwanted_words):
        super().__init__(data)
        self.clean(unwanted_words)  # Cleans the sentence by removing unwanted words.

    # Function returns true if cleaned_sentence is empty string.
    def sentence_empty(self):
        return self.cleaned_data == ""

    # Counts how many times a person's name or nickname appears in the sentence.
    def check_for_names(self, person):
        counter = 0
        for word in person.real_name.word_list:  # Checks for appearances of the real name.
            if word in self.word_list:
                counter += self.word_list.count(word)
        for nickname in person.nicknames:  # Checks for appearances of nicknames.
            if nickname.cleaned_data != "":
                if nickname.cleaned_data in self.cleaned_data:
                    counter += self.cleaned_data.count(nickname.cleaned_data)

        return counter

    # Returns true if the person (real name or nickname) appears in the sentence at least once.
    def check_if_person_in_sentence(self, person):
        for word in person.real_name.word_list:  # Checks if the real name exists in the sentence.
            if word in self.word_list:
                return True
        for nickname in person.nicknames:  # Checks if any nickname exists in the sentence.
            if nickname.cleaned_data != "":
                if nickname.cleaned_data in self.cleaned_data:
                    return True
        return False  # Returns false if the person is not found.

    # Method takes a sentence and a threshold and checks if they have at least a threshold amount of words in common.
    def sentence_is_similar(self, sentence, threshold):
        words_in_common = []
        for word in sentence.word_list:
            if word in self.word_list and word not in words_in_common:  # Avoids counting duplicate words.
                words_in_common.append(word)
        return len(words_in_common) >= threshold  # Returns true if enough words are shared.
