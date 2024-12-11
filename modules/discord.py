import requests
import json
import re

def main(account):
    username = account["username"] + "#" + account["discriminator"]
    username2 = account["global_name"]
    bio = account["bio"]
    avatar = f'https://cdn.discordapp.com/avatars/{account["id"]}/{account["avatar"]}.png'

    links = re.findall(r'(https?://[^\s]+)', bio)
    links.append(f"https://discord.com/users/{account['id']}")

    return {
        "sites_checked": [f"https://discord.com/users/{account['id']}"],
        "usernames": [username, username2],
        "images": [avatar],
        "bios": [bio],
        "links": links
    }