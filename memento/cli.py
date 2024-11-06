import os

import click
from alembic import command, config
from rich import print
from rich.prompt import Prompt

ENV_VAR = "MEMENTO_DB_CONNECTION_STRING"
CONFIG_DIR = os.path.dirname(os.path.realpath(__file__))


@click.command()
def cli():
    alembic_cfg = config.Config(f"{CONFIG_DIR}/alembic.ini")
    alembic_cfg.set_main_option("script_location", f"{CONFIG_DIR}/migrations")

    if os.getenv(ENV_VAR, None) is None:
        print(f"No connection string found at environment variable {ENV_VAR}.")
        os.environ[ENV_VAR] = Prompt.ask("Enter your database connection string")
    else:
        print(f"MEMENTO_DB_CONNECTION_STRING found.")

    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    cli()
