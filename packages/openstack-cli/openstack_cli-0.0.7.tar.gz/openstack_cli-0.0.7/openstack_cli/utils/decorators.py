import requests
import functools
import click
from openstack_cli.utils.config_tools import configtools
from openstack_cli.utils.authentication import login_process


def is_bought(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        [slug, _id] = kwargs["package"].split(":")

        cookies = {
            "access_token": configtools.get("ACCESS"),
            "refresh_token": configtools.get("REFRESH"),
            "username": configtools.get("USERNAME"),
        }
        res = requests.get(
            "https://api.openstack.sh/api/users/templates/", cookies=cookies
        )
        if res.status_code == 200:
            res = res.json()

            for item in res["results"]:
                if item["id"] == int(_id) and item["slug"] == slug:
                    return func(*args, **kwargs)

            click.echo("you have to buy this package first")
            return
        else:
            click.echo("there some problem will fix it.")
            return

    return wrapper


def is_authenticated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not configtools.is_loggedin():
            login_process()
        func(*args, **kwargs)

    return wrapper
