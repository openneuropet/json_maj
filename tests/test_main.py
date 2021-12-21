import pytest
from json_maj.main import JsonMAJ, load_json_or_dict
import json
import os

path_to_temp_json = 'temp_test_json.json'
test_data = {'test': 'this is only a test'}
path_to_temp_json_to_update_from = 'temp_test_json_to_update_from.json'


@pytest.fixture
def setup_test_data():
    with open(path_to_temp_json, 'w') as outfile:
        json.dump(test_data, outfile)


@pytest.fixture
def update_test_data():
    test_data.update({'testing_from_file': 'writing to a json file and reading back in'})
    with open(path_to_temp_json_to_update_from, 'w') as outfile:
        json.dump(test_data, outfile)


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data(request):
    def remove_test_files():
        # clean up test json
        os.remove(path_to_temp_json)
        os.remove(path_to_temp_json_to_update_from)
    request.addfinalizer(remove_test_files)


def test_JsonMAJ_load_json_or_dict(setup_test_data):
    assert load_json_or_dict(path_to_temp_json) == test_data
    assert load_json_or_dict(test_data) == test_data


def test_JsonMAJ_update_json_from_dictionary(setup_test_data, update_test_data):
    json_maj = JsonMAJ(path_to_temp_json, test_data)
    json_maj.update()

    with open(json_maj.json_path, 'r') as infile:
        updated_json = json.load(infile)

    assert updated_json == test_data


def test_JsonMAJ_update_json_from_json(setup_test_data, update_test_data):
    json_maj = JsonMAJ(path_to_temp_json, path_to_temp_json_to_update_from)
    json_maj.update()

    with open(json_maj.json_path, 'r') as infile:
        updated_from_json_file = json.load(infile)

    assert updated_from_json_file == test_data


def test_JsonMAJ_remove(setup_test_data, update_test_data):
    json_maj = JsonMAJ(path_to_temp_json, {'remove': 'we will remove this key and value for our test.'})
    json_maj.update()

    json_maj.remove('remove', 'test')

    with open(path_to_temp_json, 'r') as infile:
        test_remove_method = json.load(infile)

    # assert key is no longer in file
    with pytest.raises(KeyError):
        test_remove_method['remove']

    with pytest.raises(KeyError):
        test_remove_method['test']

    json_maj = JsonMAJ(path_to_temp_json, {'remove': 'we will remove this key and value for our test.'})
    json_maj.update()

    # test we can delete a single key
    json_maj.remove('remove')
    with open(path_to_temp_json, 'r') as infile:
        test_remove_method = json.load(infile)

    # assert key is no longer in file
    with pytest.raises(KeyError):
        test_remove_method['remove']

