import requests
import json
import utils
import bs4

def main(account):

    auth_req = requests.get("https://open.spotify.com/")

    soup = bs4.BeautifulSoup(auth_req.text, "html.parser")
    session = json.loads(soup.find("script", {"id": "session"}).text)["accessToken"]
    
    headers = {
        "Authorization": "Bearer " + session
    }
    
    response = requests.get(f"https://spclient.wg.spotify.com/user-profile-view/v3/profile/{account['id']}", headers=headers)

    name = response.json()["name"]
    try:
        image = response.json()["image_url"]
    except KeyError:
        image = None

    return {
        "sites_checked": [f"https://open.spotify.com/user/{account['id']}"],
        "names": [name],
        "images": [image],
        "links": [f"https://open.spotify.com/user/{account['id']}"]
    }