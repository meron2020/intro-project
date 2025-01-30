import csv

from Person import Person
from Sentence import Sentence


class Processor:
    @staticmethod
    def read_csv_file(file_path, unwanted_words = None):
        # Iterates over people file and adds the name to the names list
        with open(file_path, 'r', newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            lines = []
            line_type = ""
            for row in reader:
                if reader.line_num == 1:
                    if row[0] == "sentence":
                        line_type = "sentence"
                    elif row[0] == "Name":
                        line_type = "name"
                    else:
                        line_type = "common"
                else:
                    if line_type == "sentence":
                        lines.append(Sentence(row[0], unwanted_words))
                    elif line_type == "name":
                        lines.append(Person(row[0], row[1]))
                    else:
                        lines.append(row[0])
        return lines

    @staticmethod
    def split_data_to_words(data_list):
        new_data_list = []
        for data in data_list:
            data.split_data_to_words()
            new_data_list.append(data.word_list)

    @staticmethod
    def clean(data_list, common_words_list):
        for data in data_list:
            data.clean(common_words_list)

    @staticmethod
    # If two people have the same full name, keep the one that appeared first in the file.
    def remove_duplicate_names(person_list):
        unique_cleaned_names = []
        unique_names = []
        for person in person_list:
            if person.real_name.cleaned_data not in unique_cleaned_names:
                unique_names.append(person)
                unique_cleaned_names.append(person.real_name.cleaned_data)
        return unique_names


    @staticmethod
    # Remove sentences with 0 words.
    def remove_empty_sentences(sentences_list):
        for sentence in sentences_list:
            if sentence.sentence_empty():
                sentences_list.remove(sentence)

    @staticmethod
    def clean_sentences(sentences_list, common_words_list):
        Processor.clean(sentences_list, common_words_list)
        Processor.remove_empty_sentences(sentences_list)


    @staticmethod
    def output_to_json(sentences_list, name_list):
        return {"Question 1": {"Processed Sentences": [sentence.word_list for sentence in sentences_list],
                               "Processed Names": [[name.real_name.word_list,
                                                    [nickname.word_list for nickname in name.nicknames if
                                                     len(nickname.word_list) > 0]] for name in name_list]}}
