import requests
import bs4
import utils
import re

def main(account):
    data = requests.get(f"https://steamcommunity.com/profiles/{account['id']}/ajaxaliases/")

    aliases = [alias["newname"] for alias in data.json()]

    profile = requests.get(f"https://steamcommunity.com/profiles/{account['id']}")

    # profile_data = re.search(r'g_rgProfileData = (.*);', profile.text).group(1)
    # print(profile_data)
    
    soup = bs4.BeautifulSoup(profile.text, "html.parser")
    avatar = soup.find("link", {"rel": "image_src"})["href"]
    bio = soup.find("meta", {"name": "Description"})["content"]
    username = soup.find("span", {"class": "actual_persona_name"}).text

    links = re.findall(r'(https?://[^\s]+)', bio)
    links.append(f"https://steamcommunity.com/profiles/{account['id']}")

    aliases.append(username)

    return {
        "sites_checked": [f"https://steamcommunity.com/profiles/{account['id']}"],
        "usernames": aliases,
        "images": [avatar],
        "bios": [bio],
        "links": links
    }