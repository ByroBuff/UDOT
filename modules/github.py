import requests
import json
import utils
import re

def get_unique_objects(data):
    unique = {json.dumps(obj, sort_keys=True) for obj in data}
    return [json.loads(obj) for obj in unique]


def main(account):
    name_req = requests.get(f"https://api.github.com/users/{account['name']}")
    if name_req.json().get("message", "").startswith("API rate limit exceeded"):
        return None
    
    name = name_req.json()["name"]
    avatar_url = name_req.json()["avatar_url"]
    bio = name_req.json()["bio"]

    try:
        links = re.findall(r'(https?://[^\s]+)', bio)
    except:
        links = []

    location = name_req.json()["location"]
    blog = name_req.json()["blog"]
    company = name_req.json()["company"]
    twitter_username = name_req.json()["twitter_username"]

    response = requests.get(f"https://api.github.com/users/{account['name']}/events")
    data = response.json()

    commits = [commit for event in data for commit in event.get('payload', {}).get('commits', [])]
    authors = [commit.get('author') for commit in commits if commit.get('author')]
    unique_authors = get_unique_objects(authors)

    final_list = [author["email"] for author in unique_authors if author.get('name') == name]

    if twitter_username != None:
        twitter_out = utils.call("twitter", {"name": twitter_username})
    else:
        twitter_out = {}

    links.append(f"https://github.com/{account['name']}")
    links.append(blog)

    data = {
        "sites_checked": [f"https://github.com/{account['name']}"],
        "usernames": [account["name"]],
        "names": [name],
        "emails": final_list,
        "images": [avatar_url],
        "bios": [bio],
        "locations": [location],
        "links": links,
        "companies": [company]
    }

    for key in twitter_out:
        if key in data:
            data[key].extend(twitter_out[key])
        else:
            data[key] = twitter_out[key]

    return utils.clean(data)