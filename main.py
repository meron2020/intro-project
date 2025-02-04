import argparse
import os
import sys
from webbrowser import Error

from Processor import Processor
from SequenceCounter import SequenceCounter
from PersonCounter import PersonCounter
from SearchEngine import SearchEngine
from ContextFinder import ContextFinder
from DirectNeighborsFinder import DirectNeighborsFinder
from IndirectConnectionFinder import IndirectConnectionFinder
from SentenceGrouper import SentenceGrouper


def parse_arguments():
    parser = argparse.ArgumentParser(description='Example script to parse command-line arguments.')

    # Required argument for selecting which task to execute.
    parser.add_argument("-t", type=int, required=True)

    # Input files for various tasks.
    parser.add_argument("-s", nargs="+", type=valid_file, required=False)  # Sentence and name files.
    parser.add_argument("-r", type=valid_file, required=False)  # Remove words file.
    parser.add_argument("--preprocessed", type=valid_file, required=False)  # Preprocessed JSON file.

    # Additional arguments for specific tasks.
    parser.add_argument("--qsek_query_path", type=valid_file, required=False)  # Task 4: Query sequence file.
    parser.add_argument("--maxk", type=int, required=False)  # Task 5: Maximum k parameter.
    parser.add_argument("--windowsize", type=int, required=False)  # Tasks 6, 7, 8: Window size for context.
    parser.add_argument("--pairs", type=valid_file, required=False)  # Task 7: Pairs of names for checking connections.
    parser.add_argument("--maximal_distance", type=int, required=False)  # Task 7: Maximum distance for indirect connections.
    parser.add_argument("--fixed_length", type=int, required=False)  # Task 8: Fixed length path for indirect connections.
    parser.add_argument("--threshold", type=int, required=False)  # Tasks 6, 7, 8, 9: Threshold for grouping.

    return parser.parse_args()


def valid_file(path):
    if not os.path.isfile(path):  # Ensures the file exists before proceeding.
        print("invalid input")
        sys.exit(1)
    return path


def run_program():
    try:
        args_dict = vars(parse_arguments())  # Parses arguments into a dictionary.

        # Remove None values to avoid errors when accessing dictionary keys.
        provided_args = {argument: value for argument, value in args_dict.items() if value is not None}

        # Task 1: Processes text data for further analysis.
        if provided_args["t"] == 1:
            remove_words_path = provided_args["r"]
            sentence_file_path = provided_args["s"][0]
            people_file_path = provided_args["s"][1]

            print(Processor.output_to_json(sentence_file_path, people_file_path, remove_words_path))

        # Task 2: Finds common word sequences in the text.
        elif provided_args["t"] == 2:
            maxk = provided_args["maxk"]
            if "preprocessed" in provided_args and provided_args["preprocessed"] is not None:
                counter = SequenceCounter(True, preprocessed_json_file_path=provided_args["preprocessed"])
            else:
                counter = SequenceCounter(False, sentence_file=provided_args["s"][0], words_to_remove_file_path=provided_args["r"])

            result = SequenceCounter.create_final_dictionary(maxk, counter.sentences)
            print(result)


        # Task 3: Counts appearances of specific people in the text.
        elif provided_args["t"] == 3:
            if "preprocessed" in provided_args and provided_args["preprocessed"] is not None:
                counter = PersonCounter(True, preprocessed_json_file_path=provided_args["preprocessed"])
            else:
                counter = PersonCounter(False, name_file=provided_args["s"][1], sentence_file=provided_args["s"][0], words_to_remove_file_path=provided_args["r"])

            print(counter.count_person_appearances())

        # Task 4: Searches for sequences in the text.
        elif provided_args["t"] == 4:
            qseq_json_path = provided_args["qsek_query_path"]
            if "preprocessed" in provided_args and provided_args["preprocessed"] is not None:
                engine = SearchEngine(preprocessed_flag=True, preprocessed_json_file_path=provided_args["preprocessed"], seq_json_path=qseq_json_path)
            else:
                engine = SearchEngine(seq_json_path=qseq_json_path, sentence_file=provided_args["s"][0], words_to_remove_file_path=provided_args["r"], preprocessed_flag=False)

            print(engine.build_dict())

        # Task 5: Finds context (sequences) for names appearing in the text.
        elif provided_args["t"] == 5:
            maxk = provided_args["maxk"]
            if "preprocessed" in provided_args and provided_args["preprocessed"] is not None:
                context_finder = ContextFinder(preprocessed_flag=True, preprocessed_json_file_path=provided_args["preprocessed"])
            else:
                context_finder = ContextFinder(name_file=provided_args["s"][1], sentence_file=provided_args["s"][0], words_to_remove_file_path=provided_args["r"], preprocessed_flag=False)

            print(context_finder.find_all_contexts(maxk))

        # Task 6: Finds direct connections of people in the text.
        elif provided_args["t"] == 6:
            threshold = provided_args["threshold"]
            window_size = provided_args["windowsize"]
            if "preprocessed" in provided_args and provided_args["preprocessed"] is not None:
                neighbor_finder = DirectNeighborsFinder(preprocessed_flag=True, preprocessed_json_file_path=provided_args["preprocessed"], window_size=window_size, threshold=threshold)
            else:
                neighbor_finder = DirectNeighborsFinder(name_file=provided_args["s"][1], sentence_file=provided_args["s"][0], words_to_remove_file_path=provided_args["r"], preprocessed_flag=False, window_size=window_size, threshold=threshold)

            neighbor_finder.find_connections()
            print(neighbor_finder.return_connections())

        # Task 7: Finds indirect connections between people.
        elif provided_args["t"] == 7:
            maximal_distance = provided_args["maximal_distance"]
            pairs = provided_args["pairs"]
            if "preprocessed" in provided_args and provided_args["preprocessed"] is not None:
                connection_finder = IndirectConnectionFinder(True, pairs, maximal_distance, preprocessed_json_file_path=provided_args["preprocessed"])
            else:
                connection_finder = IndirectConnectionFinder(False, pairs, maximal_distance, name_file=provided_args["s"][1], sentence_file=provided_args["s"][0], words_to_remove_file_path=provided_args["r"], window_size=provided_args["windowsize"], threshold=provided_args["threshold"])

            print(connection_finder.find_indirect_connections())

        # Task 8: Finds indirect connections of a fixed length.
        elif provided_args["t"] == 8:
            pairs = provided_args["pairs"]
            fixed_length = provided_args["fixed_length"]
            if "preprocessed" in provided_args and provided_args["preprocessed"] is not None:
                connection_finder = IndirectConnectionFinder(True, pairs, preprocessed_json_file_path=provided_args["preprocessed"])
            else:
                connection_finder = IndirectConnectionFinder(False, pairs, name_file=provided_args["s"][1], sentence_file=provided_args["s"][0], words_to_remove_file_path=provided_args["r"], window_size=provided_args["windowsize"], threshold=provided_args["threshold"])

            print(connection_finder.find_indirect_connections_fixed_length(fixed_length))

        # Task 9: Groups related sentences together.
        elif provided_args["t"] == 9:
            threshold = provided_args["threshold"]
            if "preprocessed" in provided_args and provided_args["preprocessed"] is not None:
                grouper = SentenceGrouper(True, preprocessed_json_file_path=provided_args["preprocessed"], threshold=threshold)
            else:
                grouper = SentenceGrouper(False, sentence_file=provided_args["s"][0], words_to_remove_file_path=provided_args["r"], threshold=threshold)

            print(grouper.return_groups(grouper.find_interconnected_groups()))
        else:
            print("invalid input")  # Ensures an invalid task number results in an error.
            sys.exit(1)

    except Exception:
        print("invalid input")  # Handles unexpected errors gracefully.
        sys.exit(1)


if __name__ == "__main__":
    run_program()  # Runs the program when executed from the command line.
