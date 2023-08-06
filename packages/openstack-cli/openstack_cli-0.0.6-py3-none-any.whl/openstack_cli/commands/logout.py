import click
from openstack_cli.utils.authentication import logout_process


@click.command(help="logout to CLI")
def cli():
    logout_process()
    click.echo("logged out successfully")
