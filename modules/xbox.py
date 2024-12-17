from curl_cffi import requests
import utils
import json
import bs4

def main(account):
    response = requests.get(f"https://xboxgamertag.com/search/{account['name']}")

    print(response.text)

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    if "Gamertag doesn't exist" in response.text:
        return {
            "sites_checked": [f"https://xboxgamertag.com/search/{account['name']}"]
        }

    image = soup.find("img", {"class": "img-thumbnail"})["src"]
    image_url = "?url=".join(image.split("?url=")[1:]).split("&")[0]

    return {
        "sites_checked": [f"https://xboxgamertag.com/search/{account['name']}"],
        "links": [f"https://xboxgamertag.com/search/{account['name']}"],
        "images": [image_url]
    }