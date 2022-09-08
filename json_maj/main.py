import json


def load_json_or_dict(json_or_dict):
    if isinstance(json_or_dict, dict):
        return json_or_dict
    elif isinstance(json_or_dict, str):
        try:
            # try path actions on the passed variable
            with open(json_or_dict, 'r') as infile:
                loaded_json = json.load(infile)
            return loaded_json
        except FileNotFoundError:
            return {}


class JsonMAJ:
    def __init__(self, json_path, update_values={}, indent=4):
        self.json_path = json_path
        self.json_data = load_json_or_dict(self.json_path)
        self.update_values = load_json_or_dict(update_values)
        self.indent = indent

    def update(self, values=None):
        try:
            with open(self.json_path, 'r') as infile:
                try:
                    self.json_data = json.load(infile)
                except ValueError:
                    pass
        except FileNotFoundError:
            pass

        if values:
            self.json_data.update(values)
        else:
            self.json_data.update(self.update_values)

        with open(self.json_path, 'w') as outfile:
            json.dump(self.json_data, outfile, indent=self.indent, default=str)

    def remove(self, *keys):
        for key in keys:
            self.json_data.pop(key, None)

        with open(self.json_path, 'w') as outfile:
            json.dump(self.json_data, outfile, indent=self.indent, default=str)

    def get(self, *items):
        data_copy = self.json_data.copy()
        try:
            for item in items:
                data_copy = data_copy[item]
        except KeyError:
            data_copy = None
        return data_copy
