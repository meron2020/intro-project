import time

from IndirectConnectionFinder import IndirectConnectionFinder
from SentenceGrouper import SentenceGrouper


# Function to analyze changes in runtime of the sentence grouper based on changes in the inputted threshold.
def analyze_sentence_grouper_runtime():
    for i in range(3):
        start_time = time.time()
        grouper = SentenceGrouper(False, i,
                                  words_to_remove_file_path="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\REMOVEWORDS.csv",
                                  sentence_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q9_examples\\example_1\\sentences_small_1.csv")

        grouper.return_groups(grouper.find_interconnected_groups())
        end_time = time.time()

        print("Execution time:" + str(end_time - start_time))


# Function to analyze changes in runtime of the indirect connection finder based on changes in the inputted length of path.
def analyze_fixed_length_connection_finding_runtime():
    for i in range(6):
        start_time = time.time()
        counter = IndirectConnectionFinder(
            maximal_distance=1000,
            people_connections_path="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q8_examples\\example_1\\people_connections_1.json",
            preprocessed_flag=False, window_size=3, threshold=2,
            name_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q8_examples\\example_1\\people_small_1.csv",
            sentence_file="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Examples\\Q8_examples\\example_1\\sentences_small_1.csv",
            words_to_remove_file_path="C:\\Users\\TLP-001\\Documents\\Meron_Dev\\Intro_to_CS\\IntroFinalProject\\Data\\REMOVEWORDS.csv")
        counter.find_indirect_connections_fixed_length(i)
        end_time = time.time()
        print("Execution time:" + str(end_time - start_time))


