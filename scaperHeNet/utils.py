from json import dumps
from os import path


def sanitize_string(string):
    return string.replace("\n", "").replace("\t", "").replace("\r", "").strip()


def save_to_json(data: list, filename: str, force_save: bool = False):
    if not path.isfile(filename) or force_save:
        print(f"Saving {filename}")
        with open(filename, 'w') as f:
            f.write(dumps(data, indent=4))
