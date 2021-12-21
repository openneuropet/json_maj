import json
import pathlib
import os
import warnings


def load_json_or_dict(json_or_dict):
    if isinstance(json_or_dict, dict):
        return json_or_dict
    elif isinstance(json_or_dict, str):
        # try path actions on the passed variable
        with open(json_or_dict, 'r') as infile:
            loaded_json = json.load(infile)
        return loaded_json


class JsonMAJ:
    def __init__(self, json_path, update_values):
        self.json_path = json_path
        self.json_data = {}
        self.update_values = load_json_or_dict(update_values)

    def update(self):
        try:
            with open(self.json_path, 'r') as infile:
                try:
                    self.json_data = json.load(infile)
                except ValueError:
                    pass
        except FileNotFoundError:
            pass
            #warnings.warn(f"File {self.json_path} not found, creating new.")

        self.json_data.update(self.update_values)

        with open(self.json_path, 'w') as outfile:
            json.dump(self.json_data, outfile)








        return