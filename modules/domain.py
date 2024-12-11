import requests
import json
import utils

def main(account):
    return {
        "sites_checked": [f"https://{account['name']}"],
        "links": [f'https://{account["name"]}']
    }