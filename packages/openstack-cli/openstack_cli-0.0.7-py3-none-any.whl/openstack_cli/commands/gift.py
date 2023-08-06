import click
import requests
from tabulate import tabulate
from openstack_cli.utils.config_tools import configtools
from openstack_cli.utils.decorators import is_authenticated
from openstack_cli.utils.authentication import logout_process


@click.group(help="to deal with gifts/templates")
def cli():
    pass


@cli.command(
    help="show list gifts that you have, '-a' to show all gifts in openstack.sh"
)
@click.option("--all", "-a", is_flag=True, help="List all available gifts")
@is_authenticated
def ls(all):
    """show templates"""
    if all:
        res = requests.get("https://api.openstack.sh/api/templates/")
        res = res.json()

        lst = [
            [f"{x['slug']}:{x['id']}", x["description"], f"{x['price']}$", x["updated"]]
            for x in res["results"]
        ]
        headers = ["template", "description", "prices", "updated"]

        lst = sorted(lst, key=lambda l: l[0], reverse=False)
        lst = tabulate(lst, headers=headers, tablefmt="heavy_outline")

        click.echo(lst)
    else:
        cookies = {
            "access_token": configtools.get("ACCESS"),
            "refresh_token": configtools.get("REFRESH"),
            "username": configtools.get("USERNAME"),
        }
        res = requests.get(
            "https://api.openstack.sh/api/users/templates/", cookies=cookies
        )

        if res.status_code == 401:
            logout_process()
            click.echo("you have to login first")
        else:
            res = res.json()
            lst = [
                [
                    f"{x['slug']}:{x['id']}",
                    x["description"],
                    f"{x['price']}$",
                    x["updated"],
                ]
                for x in res["results"]
            ]
            headers = ["template", "description", "prices", "updated"]

            lst = sorted(lst, key=lambda l: l[0], reverse=False)
            lst = tabulate(lst, headers=headers, tablefmt="heavy_outline")

            click.echo(lst)
