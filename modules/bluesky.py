import requests
import utils
import json

def main(account):
    response = requests.get(f"https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile?actor={account['name']}")
    data = response.json()

    username = data["handle"]
    name = data["displayName"]
    avatar = data["avatar"]

    return {
        "sites_checked": [f"https://bsky.app/profile/{account['name']}"],
        "usernames": [username],
        "names": [name],
        "images": [avatar],
        "links": [f"https://bsky.app/profile/{account['name']}"]
    }