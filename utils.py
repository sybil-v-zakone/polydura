import json


def load_keys():
    with open("private_keys.txt", "r") as f:
        keys = [row.strip() for row in f]
        return keys


def load_json_file(path):
    return json.load(open(path))
