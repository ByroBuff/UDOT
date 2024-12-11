import requests
import json
import utils
import re

def main(account):
    headers = {
        'client-id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
    }

    data = '[{"operationName":"HomeOfflineCarousel","variables":{"channelLogin":"' + account["name"] + '","includeTrailerUpsell":false,"trailerUpsellVideoID":"601752619"},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"84e25789b04ac4dcaefd673cfb4259d39d03c6422838d09a4ed2aaf9b67054d8"}}},{"operationName":"ChannelPointsContext","variables":{"channelLogin":"' + account["name"] + '","includeGoalTypes":["CREATOR","BOOST"]},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"374314de591e69925fce3ddc2bcf085796f56ebb8cad67a0daa3165c03adc345"}}}]'

    response = requests.post('https://gql.twitch.tv/gql', headers=headers, data=data)

    user_info = response.json()[0]["data"]["user"]

    if user_info == None:
        return {
            "sites_checked": [f"https://twitch.tv/{account['name']}"],
        }

    profile_pic = response.json()[1]["data"]["community"]["profileImageURL"]

    login = user_info["login"]
    display_name = user_info["displayName"]
    bio = user_info["description"]
    links = []

    for social_media in user_info["channel"]["socialMedias"]:
        if social_media["name"] == "youtube":
            utils.call("youtube", {"url": social_media["url"]})
        elif social_media["name"] == "twitter":
            utils.call("twitter", {"url": social_media["url"]})
            
        links.append(social_media["url"])
    
    links.append(f"https://twitch.tv/{login}")

    return {
        "sites_checked": [f"https://twitch.tv/{login}"],
        "usernames": [login, display_name],
        "images": [profile_pic],
        "bios": [bio],
        "links": links
    }