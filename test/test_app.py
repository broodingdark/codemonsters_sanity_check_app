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


def test_run_suite():
    pytest_mock = mock.patch("app.pytest.main").start()
    path_mock = mock.patch("app.Path.resolve").start()
    path_mock.return_value = "test"
    app.run_suite()
    pytest_mock.assert_called_with(["-q", "-s", "test"])


def test_main_validate_no_config_provided():
    mock_validate_config = mock.patch("app.validate_config").start()
    arg_parser = app.init_argparse()
    args = arg_parser.parse_args(["-v"])
    app.main(args)
    mock_validate_config.assert_called_with(app.DEFAULT_CONFIG_PATH_FROM)


def test_main_validate_config_provided():
    mock_validate_config = mock.patch("app.validate_config").start()
    arg_parser = app.init_argparse()
    args = arg_parser.parse_args(["-v", "test"])
    app.main(args)
    mock_validate_config.assert_called_with("test")


def test_main_run_suite():
    mock_copy = mock.patch("app.copy").start()
    mock_run_suite = mock.patch("app.run_suite").start()
    arg_parser = app.init_argparse()
    args = arg_parser.parse_args(["-s"])
    app.main(args)
    mock_copy.assert_called()
    mock_run_suite.assert_called()
