import click


@click.command(help="show doc about openstack")
def cli():
    click.echo_via_pager(
        """
=========
openstack
=========

openstack is a poilerplate Python that encourages rapid development
and clean, pragmatic design. and we're support templates to your field
what ever you want. Thanks for checking it out.

All documentation is in the "``docs``" directory and online at
https://openstack.sh/cli/. If you're just getting started,
here's how we recommend you read the docs:
"""
)
