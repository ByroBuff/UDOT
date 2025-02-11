import json
import rich
import importlib
import re
import traceback

def load_config() -> dict:
    with open('config.json', 'r') as f:
        return json.load(f)
    
def save_config(config: dict) -> None:
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

config = load_config()

def print_logo():
    banner = """[bold]
            [blue]888     888[/][white]      888          888   [/]
            [blue]888     888[/][white]      888          888   [/]
            [blue]888     888[/][white]      888          888   [/]
            [blue]888     888[/][white]  .d88888  .d88b.  888   [/]
            [blue]888     888[/][white] d88" 888 d88""88b 888888[/]
            [blue]888     888[/][white] d88  888 888  888 888   [/]
            [blue]Y88b. .d88P[/][white] Y88b 888 Y88..88P Y88b. [/]
            [blue] "Y88888P" [/][white]  "Y88888  "888P"   "Y888[/][/bold]

                       [reset]By : [bold][deep_sky_blue1][link=https://x.com/byrobuff1]@ByroBuff[/link][/][/][/]
               [indian_red1]The best Discord osint tool 💖[/indian_red1]
    """

    rich.print(banner)

class Glyphs:
    if config["glyphs"] == True:
        LEFT_POINT =""
        RIGHT_POINT = ""
        LEFT_ROUND = ""
        RIGHT_ROUND = ""
    else:
        LEFT_POINT = "█"
        RIGHT_POINT = "█"
        LEFT_ROUND = "█"
        RIGHT_ROUND = "█"

def log(message: str, level: str = "info") -> None:
    SUCCESS = "#71f571"
    SUCCESS_DARK = "#127c12"
    INFO = "#71a3f5"
    INFO_DARK = "#123c80"
    WARN = "#f5c971"
    WARN_DARK = "#806612"
    ERROR = "#ff9696"
    ERROR_DARK = "#7d0c0c"

    if level == "success":
        rich.print(f"[{SUCCESS_DARK}]{Glyphs.LEFT_ROUND}[/{SUCCESS_DARK}][{SUCCESS} on {SUCCESS_DARK}]SUCCESS[/{SUCCESS} on {SUCCESS_DARK}][{SUCCESS_DARK}]{Glyphs.RIGHT_ROUND}[/{SUCCESS_DARK}] [{SUCCESS}]{message}[/{SUCCESS}]")
        
    elif level == "info":
        rich.print(f"[{INFO_DARK}]{Glyphs.LEFT_ROUND}[/{INFO_DARK}][{INFO} on {INFO_DARK}]INFO[/{INFO} on {INFO_DARK}][{INFO_DARK}]{Glyphs.RIGHT_ROUND}[/{INFO_DARK}] [{INFO}]{message}[/{INFO}]")

    elif level == "warn":
        rich.print(f"[{WARN_DARK}]{Glyphs.LEFT_ROUND}[/{WARN_DARK}][{WARN} on {WARN_DARK}]WARNING[/{WARN} on {WARN_DARK}][{WARN_DARK}]{Glyphs.RIGHT_ROUND}[/{WARN_DARK}] [{WARN}]{message}[/{WARN}]")

    elif level == "error":
        rich.print(f"[{ERROR_DARK}]{Glyphs.LEFT_ROUND}[/{ERROR_DARK}][{ERROR} on {ERROR_DARK}]ERROR[/{ERROR} on {ERROR_DARK}][{ERROR_DARK}]{Glyphs.RIGHT_ROUND}[/{ERROR_DARK}] [{ERROR}]{message}[/{ERROR}]")
def check_module(module_name: str) -> bool:
    try:
        importlib.import_module(f"modules.{module_name}")
        return True
    except ModuleNotFoundError:
        return False

def clean(data: dict) -> dict:

    new_dict = {}

    for key in data:
        data[key] = list(filter(None, data[key]))

    for key in data:
        data[key] = list(set(data[key]))

    for key in data:
        if data[key] != []:
            new_dict[key] = data[key]

    return new_dict

def call(module_name: str, account: dict):
    if check_module(module_name):
        log(f"Running {module_name} module...", "info")
        module = importlib.import_module(f"modules.{module_name}")
        func = getattr(module, "main")

        try:
            return func(account)
        except Exception as e:
            log(f"Error running {module_name} module:\n=============================================\n\n{traceback.format_exc()}\nPassed Info: {account}\n\n=============================================", "error")
    else:
        log(f"Module for {module_name} not found.", "warn")

def extract(text):

    if not isinstance(text, str):
        return {}

    regexes = {
        "links": r'(https?://[^\s]+)',
        "emails": r'[\w\.-]+@[\w\.-]+',
        "phone_numbers": r'\+\d{1,3}[-.\/ ]?\(?\d{1,4}\)?[-.\/ ]?\d{1,4}[-.\/ ]?\d{1,4}[-.\/ ]?\d{1,4}'
    }

    data = {}

    for key in regexes:
        if key in data:
            data[key].extend(re.findall(regexes[key], text))
        else:
            data[key] = re.findall(regexes[key], text)

    return data

def merge(data: dict, more_data: dict) -> dict:
    for key, value in more_data.items():
        if key in data:
            data[key].extend(value)
        else:
            data[key] = value

    return data

def get_module(link: str):
    modules = {
        "telegram": r"https?://(www.)?t.me/[\w]+",
        "gunslol": r"https?://(www.)?guns.lol/[\w]+",
        "linktree": r"https?://(www.)?linktr.ee/[\w]+",
        "youtube": [r"https?://(www.)?youtube.com/channel/[\w]+", r"https?://(www.)?youtube.com/c/[\w]+", r"https?://(www.)?youtube.com/@[\w]+", r'https?://(www.)?youtube.com/[\w]+'],
        "bluesky": r"http://[\w]+.bsky.social",
        "discord": r"https?://(www.)?discord.com/users/[\w]+",
        "instagram": r"https?://(www.)?instagram.com/[\w]+",
        "twitter": [r"https?://(www.)?twitter.com/[\w]+", r"https?://(www.)?x.com/[\w]+"],
        "steam": [r"https?://(www.)?steamcommunity.com/id/[\w]+", r"https?://(www.)?steamcommunity.com/profiles/[\w]+"],
        "github": r"https?://(www.)?github.com/[\w]+",
        "reddit": r"https?://(www.)?reddit.com/u?(ser)/[\w]+",
        "twitch": r"https?://(www.)?twitch.tv/[\w]+",
        "spotify": r"https?://open.spotify.com/user/[\w]+",
        "xbox": r"https?://(www.)?xboxgamertag.com/search/[\w]+",
    }

    for module in modules:
        if isinstance(modules[module], list):
            for regex in modules[module]:
                if re.match(regex, link):
                    return module
                
        elif isinstance(modules[module], str):
            if re.match(modules[module], link):
                return module

    return None

def process_module_output(source, module_output, final_output, modualised_output, checked):
    if module_output is None:
        return

    sites_checked = module_output["sites_checked"]
    checked.extend(sites_checked)

    keys = list(module_output.keys())
    keys.remove("sites_checked")

    for key in keys:
        if key not in final_output:
            final_output[key] = module_output[key]
        else:
            final_output[key] += module_output[key]

    if source not in modualised_output:
        modualised_output[source] = {}

    for key in keys:
        # add the key to source
        if key not in modualised_output[source]:
            modualised_output[source][key] = module_output[key]
        else:
            modualised_output[source][key] += module_output[key]