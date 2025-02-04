import re


class Data:
    def __init__(self, data):
        self.data = data
        self.word_list = None
        self.cleaned_data = data
        self.sequence_list = []

    # Turn all inputs to lowercase
    def convert_to_lowercase(self) -> None:
        self.cleaned_data = self.data.lower()

    # Remove all punctuation from the data and replace with whitespace.
    # Punctuation -> everything that is not numbers or letters
    def remove_punctuation(self) -> None:
        self.cleaned_data = re.sub(r'[^A-Za-z0-9]+', ' ', self.cleaned_data)

    # Remove all words that are in the unwanted words file
    def remove_unwanted_words(self, unwanted_words: list) -> None:
        if unwanted_words:
            unwanted_set = set(unwanted_words)
            words = self.cleaned_data.split()
            filtered = [word for word in words if word not in unwanted_set]
            self.cleaned_data = ' '.join(filtered)

    # remove whitespaces appearing one after the other
    def remove_consecutive_whitespaces(self):
        self.cleaned_data = re.sub(r'\s+', ' ', self.cleaned_data)

    # Function takes a sentence and splits into words and sets self.word_list
    def split_data_to_words(self) -> None:
        self.word_list = self.cleaned_data.split()

    # Iterates over sentence and checks if sequence exists in sentence
    def count_sequence_in_sequence_list(self, sequence:str) -> int:
        return sum(1 for sequence_to_check in self.sequence_list if sequence == sequence_to_check)

    # Function removes whitespace at the beginning and at the end of the sentence
    def remove_whitespace_suffix_and_prefix(self) -> None:
        self.cleaned_data = self.cleaned_data.lstrip().rstrip()

    # Function executes all cleaning functions on the inputted data.
    def clean(self, unwanted_words=None) -> None:
        # If data is empty
        if not self.data.strip():
            self.cleaned_data = ""
            self.word_list = []
            self.sequence_list = []
            return

        # Execute cleaning functions.
        self.convert_to_lowercase()
        self.remove_punctuation()
        self.remove_unwanted_words(unwanted_words)
        self.remove_consecutive_whitespaces()
        self.remove_whitespace_suffix_and_prefix()

        # No need to continue procedure if cleaned data is empty.
        if not self.cleaned_data:
            self.word_list = []
            self.sequence_list = []
            return

        # Create word list
        self.split_data_to_words()

        # Find all sequences
        for i in range(1, len(self.word_list) + 1):
            self.sequence_list.extend(self.create_sequence_list(i))

    # Function takes input with the length of sequence requested and returns a list of sequences of consecutive words with that length
    def create_sequence_list(self, seq_length: int) -> list:
        sequence_list = []
        for i in range(len(self.word_list) - seq_length + 1):
            sequence_list.append(" ".join(self.word_list[i:i + seq_length]))
        return sequence_list
