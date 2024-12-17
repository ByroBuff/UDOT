import json
import rich
import importlib
import re

def load_config() -> dict:
    with open('config.json', 'r') as f:
        return json.load(f)
    
def save_config(config: dict) -> None:
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

config = load_config()

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

        return func(account)
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
        "telegram": r"http?s://t.me/[\w]+",
        "gunslol": r"http?s://guns.lol/[\w]+",
        "linktree": r"http?s://linktr.ee/[\w]+",
        "youtube": [r"http?s://www.youtube.com/channel/[\w]+", r"http?s://www.youtube.com/c/[\w]+", r"http?s://www.youtube.com/@[\w]+"],
        "bluesky": r"http://[\w]+.bsky.social",
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

def process_module_output(module_output, final_output, checked):
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