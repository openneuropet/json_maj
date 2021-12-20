import pytest
from json_maj.main import JsonMAJ, load_json_or_dict
import json
import os

path_to_temp_json = 'temp_test_json.json'
test_data = {'test': 'this is only a test'}
path_to_temp_json_to_update_from = 'temp_test_json_to_update_from.json'

def test_JsonMAJ_load_json_or_dict():
    with open(path_to_temp_json, 'w') as outfile:
        json.dump(test_data, outfile)

    assert load_json_or_dict(path_to_temp_json) == test_data
    assert load_json_or_dict(test_data) == test_data

    # clean up test json
    os.remove(path_to_temp_json)


def test_JsonMAJ_update_json_from_dictionary():
    json_maj = JsonMAJ(path_to_temp_json, test_data)
    json_maj.update()

    with open(json_maj.json_path, 'r') as infile:
        updated_json = json.load(infile)

    assert updated_json == test_data


def test_JsonMAJ_update_json_from_json():
    test_data.update({'testing_from_file': 'writing to a json file and reading back in'})
    with open(path_to_temp_json_to_update_from, 'w') as outfile:
        json.dump(test_data, outfile)

    json_maj = JsonMAJ(path_to_temp_json, path_to_temp_json_to_update_from)
    json_maj.update()

    with open(json_maj.json_path, 'r') as infile:
        updated_from_json_file = json.load(infile)

    assert updated_from_json_file == test_data

