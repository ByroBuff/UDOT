import requests
import json
import bs4
import utils

def main(account):

    url = account["url"]

    response = requests.get(url)

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    if soup.find("a", class_="tgme_action_button_new").text != "Send Message":
        return {
            "sites_checked": [url]
        }

    try:
        name = soup.find("div", class_="tgme_page_title").text
        username = soup.find("div", class_="tgme_page_extra").text
        image = soup.find("img", class_="tgme_page_photo_image")["src"]
    except:
        return {
            "sites_checked": [url]
        }
    try:
        bio = soup.find("div", class_="tgme_page_description").text
        more_data = utils.extract(bio)
    except:
        bio = None
        more_data = {}

    data = {
        "sites_checked": [url],
        "names": [name],
        "usernames": [username],
        "images": [image],
        "bios": [bio],
    }

    data = utils.merge(data, more_data)

    return data