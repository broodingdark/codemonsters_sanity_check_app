import json
from pathlib import Path


CONFIG_NAME = "checks/config.json"


def get_config():
    p = Path(CONFIG_NAME).resolve()
    with p.open("r") as conf:
        config = json.load(conf)

    return config


CONFIG = get_config()
