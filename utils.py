import json
import rich
import importlib


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