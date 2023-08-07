import pytest
from json_maj.main import JsonMAJ, load_json_or_dict
import json
import os
import subprocess
import sys
from pathlib import Path
from tests.test_main import path_to_temp_json, test_data, path_to_temp_json_to_update_from

# get this script's path and the path to the project source files
this_scripts_path = Path(__file__)
project_dir = this_scripts_path.parent.parent
source_files_dir = project_dir / 'json_maj'


sys.path.append(str(source_files_dir))

print(source_files_dir)

@pytest.fixture(scope='session')
def setup_test_data(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('test_cli')
    with open(os.path.join(tmpdir, path_to_temp_json_to_update_from), 'w') as outfile:
        json.dump(test_data, outfile)
    return tmpdir

def test_cli_help():
    command = f"python -m json_maj.cli --help"
    output = subprocess.run(command, shell=True, cwd=project_dir)
    assert output.returncode == 0
    command = f"python  -m json_maj.cli"
    with pytest.raises(subprocess.CalledProcessError) as error:
        output = str(subprocess.check_output(command, shell=True, cwd=project_dir))
        assert error.type == subprocess.CalledProcessError
        assert error.value.code == 2
        assert 'usage: cli.py' in output


def test_cli_update_from_json(setup_test_data):
    command = f"python -m json_maj.cli {setup_test_data / 'cli_test_json.json'} --updatefile " \
              f"{setup_test_data / path_to_temp_json_to_update_from}"
    update_w_source = subprocess.run(command, shell=True)
    with open(setup_test_data / 'cli_test_json.json', 'r') as infile:
        contents = json.load(infile)
        assert test_data == contents
        assert update_w_source.returncode == 0

def test_cli_update_kwargs(setup_test_data):
    command = f"python -m json_maj.cli {setup_test_data / 'cli_test_json.json'} --kwargs Int1=1 Float1=1.0 Bool1=true " \
              f"string1='string1'"
    use_kwargs = subprocess.run(command, shell=True)
    with open(setup_test_data / 'cli_test_json.json', 'r') as infile:
        contents = json.load(infile)
        assert contents['Int1'] == 1
        assert contents['Float1'] == 1.0
        assert contents['Bool1'] == True
        assert contents['string1'] == 'string1'


def test_cli_remove(setup_test_data):
    test_cli_remove_json_path = setup_test_data / 'test_cli_remove.json'
    command = f"python -m json_maj.cli {test_cli_remove_json_path} --kwargs KeepMe='stay' " \
              f"DeleteMe='go away!' DeleteMeToo='destroy this' SaveMeForSingleDelete='please'"
    subprocess.run(command, shell=True)
    with open(test_cli_remove_json_path, 'r') as infile:
        contents = json.load(infile)
    assert contents['KeepMe'] == 'stay'
    assert contents['DeleteMe'] == 'go away!'
    assert contents['DeleteMeToo'] == 'destroy this'
    command = f"python -m json_maj.cli {test_cli_remove_json_path} --remove DeleteMe DeleteMeToo"
    subprocess.run(command, shell=True)
    with open(test_cli_remove_json_path, 'r') as infile:
        del_contents = json.load(infile)
    assert del_contents['KeepMe'] == 'stay'
    assert len(del_contents.keys()) == 2

    command = f"python -m json_maj.cli {test_cli_remove_json_path} --remove SaveMeForSingleDelete"
    subprocess.run(command, shell=True)
    with open(test_cli_remove_json_path, 'r') as infile:
        del_contents = json.load(infile)
    assert del_contents['KeepMe'] == 'stay'
    assert len(del_contents.keys()) == 1




