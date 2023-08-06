import os
import click
import requests
from halo import Halo
import zipfile
import io
from openstack_cli.utils.decorators import is_bought, is_authenticated
from openstack_cli.utils.rename_project import (
    replace_text_in_files,
    replace_file_name,
    replace_folder_name,
)
from openstack_cli.utils.themes import BlueComposure
from openstack_cli.utils.config_tools import configtools
import inquirer


@click.command(help="start new project with selected package")
@is_authenticated
def cli():
    cookies = {
        "access_token": configtools.get("ACCESS"),
        "refresh_token": configtools.get("REFRESH"),
        "username": configtools.get("USERNAME"),
    }
    res = requests.get("https://api.openstack.sh/api/users/templates/", cookies=cookies)
    res = res.json()
    if len(res["results"]) > 0:
        q = [
            inquirer.Text(
                "name_project", message="name of project (exampleapp) as default"
            ),
            inquirer.List(
                "template",
                message="select template what you what",
                choices=[
                    f"{ind+1}:{item['slug']}" for ind, item in enumerate(res["results"])
                ],
            ),
        ]
        answer = inquirer.prompt(q, theme=BlueComposure())

        [ind, name] = answer["template"].split(":")
        ind = int(ind)

        spinner = Halo(text="Checking...", spinner="dots")
        spinner.text = "Installing..."
        spinner.start()
        r = requests.get(res["results"][ind - 1]["file"])
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        spinner.stop()
        spinner.succeed("installed")

        spinner.text = "Preparing..."
        spinner.start()
        answer["name_project"] = answer["name_project"].strip()
        if answer["name_project"] != "":
            replace_text_in_files(
                os.getcwd() + f"\{name}", "exampleapp", answer["name_project"]
            )

            replace_folder_name(
                os.getcwd() + f"\{name}", "exampleapp", answer["name_project"]
            )

            replace_file_name(name, answer["name_project"], os.getcwd())

        spinner.stop()
        spinner.succeed("done")

    else:
        click.echo("you don't have any template yet.")
