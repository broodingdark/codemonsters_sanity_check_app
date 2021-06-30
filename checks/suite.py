import json
from pathlib import Path


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
