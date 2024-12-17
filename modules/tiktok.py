import requests
import utils
import json
import bs4

def main(account):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.tiktok.com/@abuwude', headers=headers)

    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    data = json.loads(soup.find_all("script", id="__UNIVERSAL_DATA_FOR_REHYDRATION__")[0].text)

    user_info = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["user"]
    
    username = user_info["uniqueId"]
    name = user_info["nickname"]
    image = user_info["avatarLarger"]
    bio = user_info["signature"]

    more_data = utils.extract(bio)

    output = {
        "sites_checked": [f"https://www.tiktok.com/@{username}"],
        "links": [f"https://www.tiktok.com/@{username}"],
        "images": [image],
        "usernames": [username],
        "names": [name],
        "bios": [bio]
    }

    output = utils.merge(output, more_data)
    return output
    
if __name__ == "__main__":
    main({"name": "test"})