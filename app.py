import sys
import argparse


__version__ = "1.0"


def init_argparse() -> argparse.ArgumentParser:
    """
    Create a parser instance
    :return: argparse.ArgumentParser
    """
    arg_parser = argparse.ArgumentParser(
        usage="python3 %(prog)s [OPTION] [CONFIG]...",
        description="A sanity check app for CodeMonsters full API."
    )
    arg_parser.add_argument("-s", "--suite", action="store_true", help="run the sanity check suite")
    arg_parser.add_argument("-v", "--validate", action="store_true", help="validate config file")
    arg_parser.add_argument("--version", action="version", version="Sanity Check App " + __version__)
    arg_parser.add_argument("config", nargs="?")

    return arg_parser


def main(args):
    pass


if __name__ == "__main__":
    parser = init_argparse()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    arguments = parser.parse_args()
    main(arguments)
