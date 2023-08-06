import argparse
import sys
from . import sealedsecret


args_parser = argparse.ArgumentParser("sealedsecretmgr")

args_parser.add_argument("-n", "--namespace", type=str, default="default")
args_parser.add_argument(
    "-o", "--output", type=str, default="yaml", dest="output_format"
)

subparsers = args_parser.add_subparsers(help="sub-command help", dest="command")

create_parser = subparsers.add_parser(
    "create", help="Print a new SealedSecret resource as JSON"
)
create_parser.add_argument("name", type=str, help="Name of SelaedSecret to create")
create_parser.add_argument("key", type=str, help="Key contained by SealedSecret")
create_parser.add_argument(
    "value", type=str, help="Unencoded value associated with key"
)
create_parser.add_argument(
    "-m",
    "--merge-into",
    type=str,
    help="Path to existing SealedSecret to merge",
    required=False,
    default="",
)

update_parser = subparsers.add_parser(
    "update",
    help="Retrieve existing SealedSecret, add or edit a key, and print the resulting SealedSecret Resource as JSON",
)
update_parser.add_argument("name", type=str, help="Name of existing SealedSecret")
update_parser.add_argument(
    "key", type=str, help="Name of new or existing key contained in SealedSecret"
)
update_parser.add_argument(
    "value", type=str, help="Unencoded value associated with key"
)

get_parser = subparsers.add_parser(
    "get", help="Retrieve a SealedSecret and by name and print the SealedSecret as JSON"
)
get_parser.add_argument("name", type=str, help="Name of existing SealedSecret")

list_parser = subparsers.add_parser(
    "list", help="List all SealedSecretsand by name along with keys in it"
)


def __main__():
    args = args_parser.parse_args(sys.argv[1:])

    if args.command == "create":
        print(
            sealedsecret.create(
                args.name,
                args.key,
                args.value,
                args.namespace,
                args.merge_into,
                args.output_format,
            )
        )
    elif args.command == "update":
        print(
            sealedsecret.update(
                args.name, args.key, args.value, args.namespace, args.output_format
            )
        )
    elif args.command == "list":
        for (name, keys) in sealedsecret.list_names(args.namespace).items():
            print(name)
            for key in keys:
                print(f"\t{key}")
    elif args.command == "get":
        print(sealedsecret.get(args.name, args.namespace, args.output_format))
