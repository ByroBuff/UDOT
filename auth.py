import requests

def validate_token(token):
    headers = {
        'authorization': token,
    }

    response = requests.get(
        f'https://discord.com/api/v9/users/@me',
        headers=headers,
    )

    return (response.status_code == 200, response.json())