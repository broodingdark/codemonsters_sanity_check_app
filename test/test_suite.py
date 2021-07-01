import json
from shutil import copy
from pathlib import Path
from unittest import mock
from requests import Response
from requests.auth import HTTPBasicAuth
from app import DEFAULT_CONFIG_PATH_FROM, DEFAULT_CONFIG_PATH_TO


def setup_module(module):
    copy(str(Path(DEFAULT_CONFIG_PATH_FROM).resolve()), str(Path(DEFAULT_CONFIG_PATH_TO).resolve()))


def teardown_module(module):
    return Path(DEFAULT_CONFIG_PATH_TO).unlink()


def teardown_function(function):
    mock.patch.stopall()


def test_get_config():
    from checks import suite
    p = Path(DEFAULT_CONFIG_PATH_FROM).resolve()
    with p.open("r") as conf:
        config = json.load(conf)
    actual_config = suite.get_config()
    assert actual_config == config


def test_send_and_validate_transaction_request_json():
    from checks import suite
    sent_json = {"foo": "bar"}
    expected_json = {"a": "b"}
    mock_post = mock.patch("checks.suite.post").start()
    mock_response = Response()
    mock_response.status_code = 200
    mock_response._content = b'{"a": "b"}'
    mock_post.return_value = mock_response

    actual_response = suite.send_and_validate_transaction("test",
                                                          sent_json,
                                                          "username",
                                                          "password",
                                                          200,
                                                          expected_json
                                                          )
    mock_post.assert_called_with("test", auth=HTTPBasicAuth("username", "password"), json=sent_json)
    assert actual_response == expected_json


def test_send_and_validate_transaction_request_text():
    from checks import suite
    sent_json = {"foo": "bar"}
    expected_text = "a, b, c"
    mock_post = mock.patch("checks.suite.post").start()
    mock_response = Response()
    mock_response.status_code = 200
    mock_response._content = b"a, b, c"
    mock_post.return_value = mock_response

    actual_response = suite.send_and_validate_transaction("test",
                                                          sent_json,
                                                          "username",
                                                          "password",
                                                          200,
                                                          expected_text
                                                          )
    mock_post.assert_called_with("test", auth=HTTPBasicAuth("username", "password"), json=sent_json)
    assert actual_response == expected_text
