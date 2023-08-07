import argparse
from json_maj.main import JsonMAJ
import sys
import ast


def very_tolerant_literal_eval(value):
    """
    Evaluates a string or string like input into a python datatype. Provides a lazy way to extract True from 'true',
    None from 'none', [0] from '[0'], etc. etc.
    :param value: the value you wish to convert to a python type
    :type value: string like, could be anything that can be evaluated as valid python
    :return: the value converted into a python object
    :rtype: depends on what ast.literal_eval determines the object to be
    """
    try:
        value = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        if str(value).lower() == 'none':
            value = None
        elif str(value).lower() == 'true':
            value = True
        elif str(value).lower() == 'false':
            value = False
        elif str(value)[0] == '[' and str(value)[-1] == ']':
            array_contents = str(value).replace('[', '').replace(']', '')
            array_contents = array_contents.split(',')
            array_contents = [str.strip(content) for content in array_contents]
            # evaluate array contents one by one
            value = [very_tolerant_literal_eval(v) for v in array_contents]
        else:
            value = str(value)
    return value

class ParseKwargs(argparse.Action):
    """
    Class that is used to extract key pair arguments passed to an argparse.ArgumentParser objet via the command line.
    Accepts key value pairs in the form of 'key=value' and then passes these arguments onto the arg parser as kwargs.
    This class is used during the construction of the ArgumentParser class via the add_argument method. e.g.:\n
    `ArgumentParser.add_argument('--kwargs', '-k', nargs='*', action=helper_functions.ParseKwargs, default={})`
    """

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            try:
                key, value = value.split('=')
                getattr(namespace, self.dest)[key] = very_tolerant_literal_eval(value)
            except ValueError:
                raise Exception(f"Unable to unpack {value}")



parser = argparse.ArgumentParser()
parser.add_argument("json", metavar="json_file", help="Json file to be updated")
parser.add_argument("--updatefile", "-f", required=False,
                    help="Json file to update from, values in this file will be inserted into "
                         "the file passed as the first argument for this cli.")
parser.add_argument('--kwargs', '-k', nargs='*', action=ParseKwargs, default={},
                    help="Include additional values into a json or override values extracted from "
                         "the supplied json. e.g. including `--kwargs TimeZero='12:12:12'` would override the "
                         "calculated TimeZero. Any number of additional arguments can be supplied after --kwargs "
                         "e.g. `--kwargs BidsVariable1=1 BidsVariable2=2` etc etc.")
parser.add_argument('--get', '-g', nargs='+', help="Checks for the value of of a key within the json.")
parser.add_argument('--remove', '-r', nargs='+', required=False,
                    help="Provide a key or several keys to be removed from a json in the form of `--remove key1 key2`. "
                         "This argument can not be used with arguments that add information to a json.")


def cli():
    args = parser.parse_args()
    if (args.remove and args.updatefile) or (args.remove and args.kwargs):
        print("You must either remove data from the json or add it, you cannot do both at the same time")
        sys.exit(1)

    if args.updatefile:
        json_maj = JsonMAJ(json_path=args.json,
                           update_values=args.updatefile)
        json_maj.update()

    if args.kwargs:
        json_maj = JsonMAJ(json_path=args.json,
                           update_values=args.kwargs)
        json_maj.update()

    if args.remove:
        json_maj = JsonMAJ(json_path=args.json)
        for remove in args.remove:
            json_maj.remove(remove)

    if args.get:
        json_maj = JsonMAJ(json_path=args.json)
        print(json_maj.get(*args.get))


if __name__ == "__main__":
    cli()
    print('debug')
