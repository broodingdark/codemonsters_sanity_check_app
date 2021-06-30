import app
import pytest
import argparse
from unittest import mock


def teardown_function(function):
    mock.patch.stopall()


def test_init_argparse():
    arg_parser = app.init_argparse()
    assert type(arg_parser) == argparse.ArgumentParser
    assert arg_parser.usage == "python3 %(prog)s [OPTION] [CONFIG]..."
    assert arg_parser.description == "A sanity check app for CodeMonsters full API."


def test_validate_config_malformed_json():
    with pytest.raises(SystemExit, match=app.CONFIG_ERROR_MESSAGE):
        app.validate_config(str(__file__))


def test_validate_config_wrong_keys():
    json_mock = mock.patch("app.json.load").start()
    json_mock.return_value = {"foo": "bar"}
    with pytest.raises(AssertionError, match=app.CONFIG_ERROR_MESSAGE):
        app.validate_config(str(__file__))
