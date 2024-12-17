import requests
import json
import utils

def main(account):
    json_data = [
        {
            'requestId': '175732666::AvatarHeadshot:150x150:webp:regular',
            'type': 'AvatarHeadShot',
            'targetId': int(account['id']),
            'size': '150x150',
        },
    ]

    response = requests.post('https://thumbnails.roblox.com/v1/batch', json=json_data)
    image = response.json()['data'][0]['imageUrl']

    user_data = requests.get(f"https://users.roblox.com/v1/users/{account['id']}")
    user_data = user_data.json()

    bio = user_data.get("description")

    more_data = utils.extract(bio)

    username = user_data.get("name")
    displayName = user_data.get("displayName")

    data = {
        "sites_checked": [f"https://www.roblox.com/users/{account['id']}"],
        "usernames": [username, displayName],
        "names": [],
        "images": [image],
        "bios": [bio],
        "links": [f"https://www.roblox.com/users/{account['id']}"]
    }

    data = utils.merge(data, more_data)
    return data