import requests
import json
import utils
import re

def main(account):
    if "id" in account:
        response = requests.get(f'https://www.youtube.com/channel/{account["id"]}')
    elif "url" in account:
        response = requests.get(account["url"])

    # find "avatarViewModel": {...} using regex
    avatar_data = json.loads(re.findall(r'"avatarViewModel":(.*?)}}},"metadata"', response.text)[0])
    avatar = avatar_data["image"]["sources"][-1]["url"]

    tokens = re.findall(r'"token":"(.*?)"', response.text)

    json_data = {
        'context': {
            'client': {
                'clientName': 'WEB',
                'clientVersion': '2.20241126.01.00',
            },
        },
        'continuation': tokens[-1]
    }



    response = requests.post(
        'https://www.youtube.com/youtubei/v1/browse?prettyPrint=False',
        json=json_data,
    )

    data = json.loads(",".join(response.text.split('"metadata":')[1].split('shareChannel')[0].split(",")[:-1]))

    username = data.get("aboutChannelViewModel", {}).get("canonicalChannelUrl").split("@")[1]
    description = data.get("aboutChannelViewModel", {}).get("description")

    

    if description:
        more_data = utils.extract(description)
    else:
        more_data = {}

    country = data.get("aboutChannelViewModel", {}).get("country")
    links = data.get("aboutChannelViewModel", {}).get("links", [])

    links = [f'https://{link["channelExternalLinkViewModel"]["link"]["content"]}' for link in links]
    page = f"https://www.youtube.com/channel/{account['id']}" if "id" in account else account["url"]

    links.append(page)

    data = {
        "sites_checked": [page],
        "usernames": [username],
        "images": [avatar],
        "bios": [description],
        "locations": [country],
        "links": links
    }

    for key in more_data:
        data[key] = more_data[key]

    return data