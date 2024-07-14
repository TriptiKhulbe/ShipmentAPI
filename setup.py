import click

from src import create_app
from src.commons.scripts import clean_db, init_db, load_csv


@click.group(name="cli")
def cli():
    pass


@cli.command(name="clean_db")
def clean_db_cli():
    create_app()
    clean_db()


@cli.command(name="init_db")
def init_db_cli():
    create_app()
    init_db()


@cli.command(name="load_csv")
@click.option("--filename", required=True)
def load_csv_cli(filename: str):
    create_app()
    load_csv(filename)


if __name__ == "__main__":
    cli()
