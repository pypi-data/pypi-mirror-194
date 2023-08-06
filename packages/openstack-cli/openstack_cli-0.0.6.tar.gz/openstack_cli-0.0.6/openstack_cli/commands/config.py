import click
from openstack_cli.utils.config_tools import configtools
from openstack_cli.utils.decorators import is_authenticated


@click.group(help="to deal with configs")
def cli():
    """all configs"""
    pass


@cli.command(help="list all configurations.")
@is_authenticated
def ls():
    configtools.list()


@cli.command(help="to get configurations variable")
@click.argument("key")
@is_authenticated
def get(key):
    click.echo(configtools.get(key))


@cli.command(help="to set configurations variable")
@click.argument("key")
@click.argument("value")
@is_authenticated
def set(key, value):
    configtools.set(key, value)
