import json

# Generic function that loads the json dictionary from a json file.
def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
