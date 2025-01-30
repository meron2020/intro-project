class SentenceWindow:
    def __init__(self, sentences):
        self.sentences = sentences

    # Function iterates over sentences and finds if person exists in window
    def find_person_in_window(self, person):
        for sentence in self.sentences:
            if sentence.check_if_person_in_sentence(person):
                return True
        return False


