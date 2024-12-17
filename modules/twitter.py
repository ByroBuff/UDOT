import requests
import user_agent
import bs4
import json
import utils
import rich
import tweeterpy



def main(account):
    twitter = tweeterpy.TweeterPy(log_level="CRITICAL")

    if "name" in account:
        username2 = account["name"]
    elif "url" in account:
        username2 = account["url"].split("/")[-1]

    try:
        user = twitter.get_user_data(username2)
    except:
        return {
            "sites_checked": [f"https://twitter.com/{username2}"]
        }

    username = user["legacy"]["screen_name"]
    name = user["legacy"]["name"]
    bio = user["legacy"]["description"]
    location = user["legacy"]["location"]
    image = user["legacy"]["profile_image_url_https"].replace("_normal", "")

    links = []

    if "description" in user["legacy"]["entities"]:
        for url in user["legacy"]["entities"]["description"]["urls"]:
            links.append(url["expanded_url"])

    if "url" in user["legacy"]["entities"]:
        for url in user["legacy"]["entities"]["url"]["urls"]:
            links.append(url["expanded_url"])

    more_data = utils.extract(bio)
    even_more_data = utils.extract(location)

    data = {
        "sites_checked": [f"https://twitter.com/{username2}"],
        "usernames": [username],
        "names": [name],
        "images": [image],
        "bios": [bio],
        "locations": [location],
        "links": links
    }

    data = utils.merge(data, more_data)
    data = utils.merge(data, even_more_data)
    return data