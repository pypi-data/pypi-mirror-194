import click
import requests
import os
from utils import get_config
from rich.console import Console

console = Console()


@click.command()
@click.argument("file", required=True)
def submit(file: str):
    slash = "/" if os.name == "posix" else "\\\\"

    data = get_config(console)
    if data is None:
        return

    cf_dir = data.get("dir")
    if cf_dir is None:
        console.print("[bold red]ERROR: [/]The default directory for parsing is not set.\nPlease run the `cf config` command.")
        return

    current_dir = os.getcwd()
    if not current_dir.startswith(cf_dir) and current_dir != cf_dir:
        console.print("[bold red]ERROR: [/]The current directory is not a contest directory.\n")
        return

    c_id = current_dir.split(slash)[-1]
    if not c_id.isdigit():
        console.print("[bold red]ERROR: [/]The current directory is not a contest directory.\n")
        return

    if not os.path.isfile(file):
        console.print("[bold red]ERROR: [/]The file does not exist.\n")
        return

    p_id = file.split(".")[0].lower()
    p_ext = file.split(".")[-1]

    # get CSRF token, RCPC something and all other shit using username, pass
    csrf = ""
    url = f"https://codeforces.com/contest/{c_id}/problem/{p_id}?csrf={csrf}"
    resp = requests.post(url=url)
