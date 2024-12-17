import requests
import utils
import json
import bs4
import rich
import re

def main(account):
    url = account["url"]

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    scripts = soup.find_all("script")

    for script in scripts:
        if script.text.startswith('self.__next_f.push([1,"6'):
            data = script.text.split('self.__next_f.push([1,"6:')[1][:-5].replace('\\"', '"')
            data = json.loads(data)[3]["data"]

            links = []

            username = data["username"]
            name = data["config"]["display_name"]
            bio = data["config"]["description"]

            more_data = utils.extract(bio)

            avatar = data["config"]["avatar"]
            email = None

            for social in data["config"]["socials"]:
                if re.match(r'https?://', social["value"]):
                    links.append(social["value"])

                elif social["social"] == "email":
                    email = social["value"]

            out = {
                "sites_checked": [url],
                "names": [name],
                "usernames": [username],
                "images": [avatar],
                "bios": [bio],
                "emails": [email],
                "links": links
            }

            out = utils.merge(out, more_data)
            return out