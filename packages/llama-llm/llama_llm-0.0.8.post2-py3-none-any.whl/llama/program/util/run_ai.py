
import requests
import os
from llama.program.util.config import get_config


def query_run_program(params):
    key, url = get_url_and_key()
    resp = powerml_run_program(params, url, key)
    return resp


def powerml_run_program(params, url, key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key,
    }
    response = requests.post(
        url=url + "/v1/run_llama_program",
        headers=headers,
        json=params)
    if response.status_code != 200:
        try:
            description = response.json()
            print(description)
        except BaseException:
            description = response.status_code
        finally:
            raise Exception(f"API error {description}")
    return response


def get_url_and_key():
    cfg = get_config()
    environment = os.environ.get("LLAMA_ENVIRONMENT")
    if environment == "LOCAL":
        key = 'test_token'
        if 'local' in cfg:
            if 'key' in cfg["local"]:
                key = cfg['local.key']
        url = "http://localhost:5001"
    elif environment == "STAGING":
        key = cfg['staging.key']
        url = 'https://api.staging.powerml.co'
    else:
        key = cfg['production.key']
        url = 'https://api.powerml.co'
    return (key, url)
