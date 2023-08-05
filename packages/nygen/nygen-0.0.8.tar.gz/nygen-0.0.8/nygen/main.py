import argparse

from nygen.conf import init_conf
from nygen.lib.formatter import Formatter
from nygen.lib.gen import gen_project
from nygen.lib.exceptions import GenException


def parse_args() -> tuple[str, dict[str, str], dict[str, str]]:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("name", help="Package name")
    for arg_name in Formatter.cmd_vars:
        create_parser.add_argument(f"--{arg_name}")

    init_parser = subparsers.add_parser("init")
    for arg_name in Formatter.conf_vars:
        init_parser.add_argument(f"--{arg_name}")

    args = parser.parse_args()
    args_dict = vars(args)

    cmd_args: dict[str, str] = {}
    for arg_name in Formatter.conf_vars:
        if arg_name in args_dict:
            cmd_args[arg_name] = args_dict[arg_name]
    args.cmd_args = cmd_args

    conf_args: dict[str, str] = {}
    for arg_name in Formatter.conf_vars:
        if arg_name in args_dict:
            conf_args[arg_name] = args_dict[arg_name]
    args.conf_args = conf_args

    return args


def main():
    args = parse_args()

    if args.command == "init":
        print("Creating conf file")
        confpath = init_conf(args.conf_args)
        print(f"Created {confpath}")
    elif args.command == "create":
        try:
            gen_project(args.name, args.cmd_args)
        except GenException as e:
            print(e)
    else:
        print("Invalid Command")


if __name__ == "__main__":
    main()
