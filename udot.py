import requests
import argparse
import auth
import utils
import rich

def get_discord_user(id: int) -> dict:
    final_output = {}
    modualised_output = {}

    headers = {
        'authorization': config["token"]
    }

    response = requests.get(f'https://discord.com/api/v9/users/{id}/profile', headers=headers)

    if response.status_code == 404:
        utils.log("User not found. Use an account that has seen this user in a guild or is friends with this user", "error")
        exit()

    checked = []

    data = response.json()
    utils.log(f"User with id {id} identified as {data['user']['username']}#{data['user']['discriminator']}.", "success")

    utils.log("Starting search...\n", "info")

    discord_data = utils.call("discord", data["user"])
    checked.append(f"https://discord.com/users/{id}")

    accounts = data["connected_accounts"]
    for account in accounts:
        module_output = utils.call(account["type"], account)
        utils.process_module_output(account["type"], module_output, final_output, modualised_output, checked)

    discord_keys = list(discord_data.keys())
    discord_keys.remove("sites_checked")

    for key in discord_keys:
        if key not in final_output:
            final_output[key] = discord_data[key]
        else:
            final_output[key] += discord_data[key]

    if "discord" not in modualised_output:
        modualised_output["discord"] = {}

    for key in discord_keys:
        if key not in modualised_output["discord"]:
            modualised_output["discord"][key] = discord_data[key]
        else:
            modualised_output["discord"][key] += discord_data[key]

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
                    utils.process_module_output(out, extra_module_output, final_output, modualised_output, checked)

    # clean each module's output
    for key in modualised_output:
        modualised_output[key] = utils.clean(modualised_output[key])

    return {
        "modular": modualised_output,
        "grouped": utils.clean(final_output)
    }

def search(id: int):
    user_data = get_discord_user(id)
    rich.print_json(data=user_data["grouped"])

if __name__ == "__main__":
    utils.print_logo()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    parser_login = subparsers.add_parser("login", help="Login to your discord account")
    parser_login.add_argument("token", help="Your discord token")

    parser_search = subparsers.add_parser("search", help="Search for a user")
    parser_search.add_argument("id", help="The user's discord id")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        exit()

    if args.command == "login":

        valid, data = auth.validate_token(args.token)
        if valid:
            utils.log(f"Successfully logged in as {data['username']}#{data['discriminator']}", "success")
            config = utils.load_config()
            config["token"] = args.token
            utils.save_config(config)
        else:
            utils.log("Invalid token.", "error")
            exit()

        exit()

    elif args.command == "search":

        config = utils.load_config()

        if config["token"] == "":
            utils.log("No token found. Please login using 'python main.py login'", "error")
            exit()

        valid, data = auth.validate_token(config["token"])
        if not valid:
            utils.log("Invalid token.", "error")
            exit()
        else:
            utils.log("Logged in as " + data["username"] + "#" + data["discriminator"], "success")
            search(args.id)
