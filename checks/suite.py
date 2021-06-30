import json
from pathlib import Path
from requests import post
from requests.auth import HTTPBasicAuth


CONFIG_NAME = "checks/config.json"


def get_config():
    p = Path(CONFIG_NAME).resolve()
    with p.open("r") as conf:
        config = json.load(conf)

    return config


CONFIG = get_config()
USERNAME = CONFIG["credentials"]["username"]
PASSWORD = CONFIG["credentials"]["password"]
ROOT = CONFIG["endpoints"]["root"]
PAYMENT_TRANSACTIONS_ENDPOINT = CONFIG["endpoints"]["payment_transactions"]
SALE_REQUEST_DATA = CONFIG["test_data"]["valid_sale_transaction"]
VOID_REQUEST_DATA = CONFIG["test_data"]["valid_void_transaction"]
SALE_SUCCESS_RESPONSE_DATA = CONFIG["expected_responses"]["sale_transaction_success"]
VOID_SUCCESS_RESPONSE_DATA = CONFIG["expected_responses"]["void_transaction_success"]
SALE_ERROR_RESPONSE_DATA = CONFIG["expected_responses"]["sale_transaction_error"]
VOID_ERROR_RESPONSE_DATA = CONFIG["expected_responses"]["void_transaction_error"]
COMPLETE_PAYMENT_TRANSACTIONS_ENDPOINT = ROOT + PAYMENT_TRANSACTIONS_ENDPOINT


def setup_module(module):
    print("Sanity Suite started!")


def teardown_module(module):
    return Path(CONFIG_NAME).unlink()


def send_and_validate_transaction(endpoint, data, username, password, expected_code, expected_data):
    """
    Main function ot use for polling the API and validating the response.
    Return value depends on the expected_data argument: if JSON is expected,
    function tries to return JSON; if text is expected, function tries to return text.
    :param endpoint: full URL endpoint
    :param data: JSON data used for the request
    :param username: username for auth
    :param password: password for auth
    :param expected_code: expected response code
    :param expected_data: expected response data
    :return: str or dict
    """
    response = post(endpoint, json=data, auth=HTTPBasicAuth(username, password))
    print("API response: " + response.text)
    assert response.status_code == expected_code

    if type(expected_data) is dict:
        processed_response = response.json()
        assert processed_response is not None
        actual_keys = processed_response.keys()
        expected_keys = expected_data.keys()
        assert all(k in actual_keys for k in expected_keys)
    else:
        processed_response = response.text.strip()
        assert processed_response == expected_data

    return processed_response
