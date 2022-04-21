import argparse
from json_maj.main import JsonMAJ
import sys


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


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
parser.add_argument('--get', '-g', help="Checks for the value of of a key within the json.")
parser.add_argument('--remove', '-r', nargs='*', required=False,
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
        json_maj = JsonMAJ()
        json_maj.remove(args.remove)

    if args.get:
        json_maj = JsonMAJ(json_path=args.json)
        print(json_maj.get(args.get))


if __name__ == "__main__":
    cli()
