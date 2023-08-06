import click
from openstack_cli.utils.authentication import login_process
from openstack_cli.utils.config_tools import configtools


@click.command(help="login to CLI")
def cli():
    if configtools.is_loggedin():
        click.echo("you're already logged in")
    else:
        login_process()
