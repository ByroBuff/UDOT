import requests
import utils
import json
import re

def main(account):

    if "name" in account:
        initial_username = account["name"]
    elif "url" in account:
        initial_username = account["url"].split("://")[1]

    response = requests.get(f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={initial_username}")
    data = response.json()

    username = data["handle"]
    name = data["displayName"]
    avatar = data["avatar"]

    return {
        "sites_checked": [f"https://bsky.app/profile/{initial_username}"],
        "usernames": [username],
        "names": [name],
        "images": [avatar],
        "links": [f"https://bsky.app/profile/{initial_username}"]
    }