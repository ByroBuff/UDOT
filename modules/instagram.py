import requests
import json
import utils
from urllib.parse import quote_plus

def get_user_id(username, session_id):
    headers = {"User-Agent": "iphone_ua", "x-ig-app-id": "936619743392459"}
    response = requests.get(
        f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username["name"]}',
        headers=headers,
        cookies={'sessionid': session_id}
    )

    try:
        if response.status_code == 404:
            return {"id": None, "error": "User not found"}

        user_id = response.json()["data"]['user']['id']
        return {"id": user_id, "error": None}

    except json.JSONDecodeError:
        return {"id": None, "error": "Rate limit"}

def get_user_info(search, session_id):
    data = get_user_id(search, session_id)
    if data["error"]:
        return data
    user_id = data["id"]

    try:
        response = requests.get(
            f'https://i.instagram.com/api/v1/users/{user_id}/info/',
            headers={'User-Agent': 'Instagram 64.0.0.14.96'},
            cookies={'sessionid': session_id}
        )
        if response.status_code == 429:
            return {"user": None, "error": "Rate limit"}

        response.raise_for_status()

        user_info = response.json().get("user")
        if not user_info:
            return {"user": None, "error": "Not found"}

        user_info["userID"] = user_id
        return {"user": user_info, "error": None}

    except requests.exceptions.RequestException:
        return {"user": None, "error": "Not found"}

def advanced_lookup(username):
    data = "signed_body=SIGNATURE." + quote_plus(json.dumps(
        {"q": username, "skip_recovery": "1"},
        separators=(",", ":")
    ))
    response = requests.post(
        'https://i.instagram.com/api/v1/users/lookup/',
        headers={
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 101.0.0.15.120",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-IG-App-ID": "124024574287414",
            "Accept-Encoding": "gzip, deflate",
            "Host": "i.instagram.com",
            "Connection": "keep-alive",
            "Content-Length": str(len(data))
        },
        data=data
    )

    try:
        return {"user": response.json(), "error": None}
    except json.JSONDecodeError:
        return {"user": None, "error": "Rate limit"}

def main(account):
    config = utils.load_config()

    if config["instagram_session"]:
        session_id = config["instagram_session"]

        info = get_user_info(account, session_id)
        if not info.get("user"):
            utils.log(info["error"], "error")
            return

        user_info = info["user"]

        name = user_info['full_name']
        url = user_info.get("external_url")
        bio = user_info.get("biography")
        public_email = user_info.get("public_email")
        public_phone_number = f"+{user_info['public_phone_country_code']} {user_info['public_phone_number']}" if user_info.get("public_phone_number") else None

        additional_info = advanced_lookup(user_info['username'])

        if additional_info["error"] == "Rate limit":
            utils.log("Rate limit exceeded. Please try again later.", "warn")

        elif "message" in additional_info["user"]:
            utils.log(additional_info["user"]["message"], "info")

        else:
            obfuscated_email = additional_info["user"].get("obfuscated_email")
            obfuscated_phone = additional_info["user"].get("obfuscated_phone")

        pfp = user_info['hd_profile_pic_url_info']['url']

        return {
            "sites_checked": [f"https://instagram.com/{account['name']}"],
            "usernames": [account["name"]],
            "names": [name],
            "images": [pfp],
            "bios": [bio],
            "emails": [public_email, obfuscated_email],
            "phone_numbers": [public_phone_number, obfuscated_phone],
            "links": [url, f"https://instagram.com/{account['name']}"]
        }
    else:
        utils.log("Instagram session not found in config.json. Not all information will be available.", "warn")

    