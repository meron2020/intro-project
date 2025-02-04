import csv
import json

from Person import Person
from Sentence import Sentence


class Processor:
    @staticmethod
    def read_csv_file(file_path, unwanted_words=None):
        # Reads the CSV file and processes it based on its type (sentence, name, or common words).
        with open(file_path, 'r', newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            lines = []
            line_type = ""
            for row in reader:
                if reader.line_num == 1:  # Determines the type of data in the file based on the header.
                    if row[0] == "sentence":
                        line_type = "sentence"
                    elif row[0] == "Name":
                        line_type = "name"
                    else:
                        line_type = "common"
                else:
                    if line_type == "sentence":
                        lines.append(Sentence(row[0], unwanted_words))  # Creates a Sentence object.
                    elif line_type == "name":
                        lines.append(Person(row[0], row[1]))  # Creates a Person object with a main name and other names.
                    else:
                        lines.append(row[0])  # Adds common words directly as strings.
        return lines

    @staticmethod
    def clean(data_list, common_words_list):
        # Cleans each item in the provided data list using the list of common words.
        for data in data_list:
            data.clean(common_words_list)

    @staticmethod
    # If two people have the same full name, keep the one that appeared first in the file.
    def remove_duplicate_names(person_list):
        unique_cleaned_names = []
        unique_names = []
        for person in person_list:
            if person.real_name.cleaned_data not in unique_cleaned_names:
                unique_names.append(person)  # Keeps the first occurrence of each unique name.
                unique_cleaned_names.append(person.real_name.cleaned_data)
        return unique_names

    @staticmethod
    # Remove sentences with 0 words.
    def remove_empty_sentences(sentences_list):
        for sentence in sentences_list:
            if sentence.sentence_empty():
                sentences_list.remove(sentence)  # Removes sentences that became empty after cleaning.

    # Function takes a list of sentences and a list of common words, cleans each sentence and then removes the empty
    # sentences from the list.
    @staticmethod
    def clean_sentences(sentences_list, common_words_list):
        Processor.clean(sentences_list, common_words_list)
        Processor.remove_empty_sentences(sentences_list)

    # Function returns the preprocessed names and sentences in the JSON format as needed.
    @staticmethod
    def output_to_json(sentence_file_path, people_file_path, remove_words_path):
        sentences_list = Processor.read_csv_file(sentence_file_path)
        name_list = Processor.read_csv_file(people_file_path)
        common_words = Processor.read_csv_file(remove_words_path)

        Processor.clean(sentences_list, common_words)  # Cleans sentences by removing common words.
        Processor.clean(name_list, common_words)  # Cleans names by removing common words.
        Processor.remove_empty_sentences(sentences_list)  # Removes any sentences that are empty after cleaning.
        Processor.remove_duplicate_names(name_list)  # Ensures names are unique after cleaning.

        return json.dumps({
            "Question 1": {
                "Processed Sentences": [sentence.word_list for sentence in sentences_list],
                "Processed Names": [
                    [name.real_name.word_list,  # Stores the main name.
                     [nickname.word_list for nickname in name.nicknames if len(nickname.word_list) > 0]]  # Stores valid nicknames.
                    for name in name_list
                ]
            }
        })
