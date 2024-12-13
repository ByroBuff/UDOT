import requests
import bs4
import utils
import re

def main(account):
    data = requests.get(f"https://steamcommunity.com/profiles/{account['id']}/ajaxaliases/")

    aliases = [alias["newname"] for alias in data.json()]

    profile = requests.get(f"https://steamcommunity.com/profiles/{account['id']}")
    
    soup = bs4.BeautifulSoup(profile.text, "html.parser")

    try:
        div = soup.find("div", {"class": "header_real_name"})
        location = div.text.strip()
    except:
        location = None

    try:
        avatar = soup.find("link", {"rel": "image_src"})["href"]
    except:
        avatar = None

    try:
        bio = soup.find("meta", {"name": "Description"})["content"]
        more_data = utils.extract(bio)
        more_data["links"].append(f"https://steamcommunity.com/profiles/{account['id']}")
    except:
        bio = None
        
    username = soup.find("span", {"class": "actual_persona_name"}).text

    aliases.append(username)

    data = {
        "sites_checked": [f"https://steamcommunity.com/profiles/{account['id']}"],
        "usernames": aliases,
        "images": [avatar],
        "locations": [location],
        "bios": [bio],
    }

    for key in more_data:
        data[key] = more_data[key]

    return data