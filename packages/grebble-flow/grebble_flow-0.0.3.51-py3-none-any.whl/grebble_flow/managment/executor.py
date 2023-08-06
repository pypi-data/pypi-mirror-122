import logging

import click

from grebble_flow.transport import manager


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--port", help="Port", type=int, default=5000,
)
@click.option(
    "--debug",
    help="Debug",
    type=bool,
    default=False,
    required=False,
    show_default=True,
)
@click.option(
    "--socket",
    help="Socket",
    type=str,
    default=False,
    required=False,
    show_default=True,
)
@click.option(
    "--max_workers",
    help="Max workers",
    type=int,
    default=False,
    required=False,
    show_default=True,
)
def run(port=5000, debug=False, socket=False, max_workers=2):
    print("Starting processors server")
    max_workers = max_workers or 2
    manager.start_server(port, max_workers)
