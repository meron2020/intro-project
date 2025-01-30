import json


class JsonManager:
    def __init__(self):
        pass

    def output_to_json(self):
        pass

    # Load JSON file into a dictionary


def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
