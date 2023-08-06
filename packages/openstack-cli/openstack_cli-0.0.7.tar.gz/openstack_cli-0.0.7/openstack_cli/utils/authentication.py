import click
import requests
from openstack_cli.utils.config_tools import configtools


def check_user_exist(username, password):
    """send post request to server to check if user exist or not."""

    res = requests.post(
        "https://api.openstack.sh/api/auth/login/",
        data={"username": username, "password": password},
    )
    
    if res.status_code == 200:
        return (True, res.json()["access_token"], res.json()["refresh_token"])
    else:
        return (False,)


def login_process():
    """login to openstack.sh CLI"""
    username = click.prompt("username", type=str)
    password = click.prompt("password", type=str, hide_input=True)

    res = check_user_exist(username, password)

    if res[0]:
        configtools.set("USERNAME", username)
        configtools.set("IS_LOGGEDIN", True)
        configtools.set("ACCESS", res[1])
        configtools.set("REFRESH", res[2])
        click.secho("successful login", fg="green")
    else:
        configtools.set("USERNAME", "")
        configtools.set("IS_LOGGEDIN", False)
        configtools.set("ACCESS", "")
        configtools.set("REFRESH", "")
        click.secho(
            "username or password is wrong. \n \
             register on website if you don't have account, you can hit this command 'openstack register' .",
            fg="red",
        )


def logout_process():
    configtools.set("USERNAME", "")
    configtools.set("ACCESS", "")
    configtools.set("REFRESH", "")
    configtools.set("IS_LOGGEDIN", False)
