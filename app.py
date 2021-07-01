import sys
import json
import pytest
import argparse
from shutil import copy
from pathlib import Path


__version__ = "1.0"
DEFAULT_CONFIG_PATH_FROM = "config.json"
DEFAULT_CONFIG_PATH_TO = "checks/config.json"
SUITE_LOCATION = "checks/suite.py"
CONFIG_ERROR_MESSAGE = "Invalid config! Please use the default one for reference!"


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


def validate_config(conf_path) -> dict:
    """
    Validate provided config file that it is a valid JSON file
    and contains the expected keys
    :param conf_path: path to file
    :return: dict
    """
    path_from = Path(conf_path).resolve()
    with path_from.open("r") as conf:
        try:
            config = json.load(conf)
        except json.decoder.JSONDecodeError:
            sys.exit(CONFIG_ERROR_MESSAGE)

    expected_keys = ["credentials", "endpoints", "test_data", "expected_responses"]
    actual_keys = config.keys()
    assert all(k in actual_keys for k in expected_keys), CONFIG_ERROR_MESSAGE

    return config


def run_suite():
    """
    Run sanity check suite
    """
    pytest.main(["-q", "-s", str(Path(SUITE_LOCATION).resolve())])


def main(args):
    if not args.config:
        conf_path = DEFAULT_CONFIG_PATH_FROM
    else:
        conf_path = args.config

    if args.validate:
        validate_config(conf_path)
    if args.suite:
        validate_config(conf_path)
        copy(Path(conf_path).resolve(), Path(DEFAULT_CONFIG_PATH_TO).resolve())
        run_suite()


if __name__ == "__main__":
    parser = init_argparse()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    arguments = parser.parse_args()
    main(arguments)
