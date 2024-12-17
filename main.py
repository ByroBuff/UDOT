import requests
import argparse
import auth
import utils
import rich

def get_discord_user(id: int):
    final_output = {}

    utils.log(f"Getting user with id {id}...", "info")

    headers = {
        'authorization': config["token"]
    }

    response = requests.get(f'https://discord.com/api/v9/users/{id}/profile', headers=headers)

    if response.status_code == 404:
        utils.log("User not found. Use an account that has seen this user in a guild or is friends with this user", "error")
        exit()

    checked = []

    data = response.json()
    utils.log(f"User {data['user']['username']}#{data['user']['discriminator']} found.\n", "success")

    discord_data = utils.call("discord", data["user"])
    checked.append(f"https://discord.com/users/{id}")

    accounts = data["connected_accounts"]
    for account in accounts:
        module_output = utils.call(account["type"], account)
        utils.process_module_output(module_output, final_output, checked)

    discord_keys = list(discord_data.keys())
    discord_keys.remove("sites_checked")

    for key in discord_keys:
        if key not in final_output:
            final_output[key] = discord_data[key]
        else:
            final_output[key] += discord_data[key]

    diff = True

    while diff != set():
        diff = set(final_output["links"]) - set(checked)
        diff = set(filter(None, diff))
        if diff:
            for link in diff:
                utils.log(f"New link found in iteration: {link}")

        if diff != set():
            for link in diff:
                if link in checked:
                    continue
                out = utils.get_module(link)
                checked.append(link)
                if out is not None:
                    extra_module_output = utils.call(out, {"url": link})
                    utils.process_module_output(extra_module_output, final_output, checked)

    rich.print_json(data=utils.clean(final_output))

def main(id: int):
    get_discord_user(id)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get a discord user's profile")
    parser.add_argument("id", type=int, help="The user's id")
    args = parser.parse_args()

    config = utils.load_config()

    if config["token"] == "":
        token = input("Enter your token: ")

        if auth.validate_token(token)[0]:
            utils.log("Token is valid and has been saved to config.json")
            config["token"] = token
            utils.save_config(config)
        else:
            utils.log("Invalid token.", "error")
            exit()

        utils.log("First run setup complete!", "success")

    utils.log("Validating token...", "info")
    valid, data = auth.validate_token(config["token"])
    if not valid:
        utils.log("Invalid token.", "error")
        exit()
    else:
        utils.log("Logged in as " + data["username"] + "#" + data["discriminator"] + "\n", "success")
        main(args.id)
