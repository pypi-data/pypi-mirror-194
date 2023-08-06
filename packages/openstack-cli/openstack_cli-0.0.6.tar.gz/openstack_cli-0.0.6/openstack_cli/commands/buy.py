import click
import inquirer
from openstack_cli.utils.themes import BlueComposure
import requests


@click.command(help="buy gift.")
def cli():
    res = requests.get("https://api.openstack.sh/api/templates/")
    res = res.json()


    q = [
        inquirer.List(
            "template",
            message="select template what you what",
            choices=[
                f"{ind+1}:{item['slug']}" for ind, item in enumerate(res["results"])
            ],
        )
    ]
    answer = inquirer.prompt(q, theme=BlueComposure())
    [ind, name] = answer["template"].split(":")
    ind = int(ind)
    click.launch(f"https://openstack.sh/template/{res['results'][ind-1]['id']}")
