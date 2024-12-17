import requests
import json
import utils

def main(account):
    url = f"https://api.reddit.com/user/{account['name']}/about/"

    response = requests.get(url)

    try:
        data = response.json()["data"]["subreddit"]
    except KeyError:
        return {
            "sites_checked": [url]
        }

    username = data["display_name_prefixed"]
    image = data["icon_img"].split("?")[0]
    bio = data["public_description"]

    more_data = utils.extract(bio)

    data = {
        "sites_checked": [url],
        "usernames": [username],
        "images": [image],
        "bios": [bio]
    }

    data = utils.merge(data, more_data)
    return data