import requests
import utils
import json
import bs4
import rich

def main(account):
    url = account["url"]

    response = requests.get(url)

    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    data = soup.find("script", id="__NEXT_DATA__").text

    data = json.loads(data)["props"]["pageProps"]

    links = []

    username = data["username"]
    image = data["profilePictureUrl"]
    name = data["pageTitle"]
    bio = data["description"]

    more_data = utils.extract(bio)

    for link in data["links"]:
        links.append(link["url"])

    for link in data["socialLinks"]:
        links.append(link["url"])

    links.append(url)

    out = {
        "sites_checked": [url],
        "names": [name],
        "usernames": [username],
        "images": [image],
        "bios": [bio],
        "links": links
    }

    out = utils.merge(out, more_data)
    return out