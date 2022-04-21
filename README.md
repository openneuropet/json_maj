# json_maj
It updates the jsons! That's it!

## Usage

```bash
usage: cli.py [-h] [--updatefile UPDATEFILE] [--kwargs [KWARGS ...]] [--remove [REMOVE ...]] json_file

positional arguments:
  json_file             Json file to be updated

optional arguments:
  -h, --help            show this help message and exit
  --updatefile UPDATEFILE, -f UPDATEFILE
                        Json file to update from, values in this file will be inserted into the file passed as the first
                        argument for this cli.
  --kwargs [KWARGS ...], -k [KWARGS ...]
                        Include additional values into a json or override values extracted from the supplied json. 
                        e.g. including `--kwargs TimeZero='12:12:12'` would override the calculated TimeZero. 
                        Any number of additional arguments can be supplied after --kwargs 
                        e.g. `--kwargs BidsVariable1=1 BidsVariable2=2` etc etc.
  --remove [REMOVE ...], -r [REMOVE ...]
                        Provide a key or several keys to be removed from a json in the form of `--remove key1 key2`. 
                        This argument can not be used with arguments that add information to a json.
```