import click


@click.command(help="Register to openstack.sh website")
def cli():
    click.launch("https://openstack.sh/register/")
