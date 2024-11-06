import os

import click
from alembic import command, config
from rich import print as rprint
from rich.prompt import Prompt

ENV_VAR = "MEMENTO_DB_CONNECTION_STRING"
CONFIG_DIR = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.argument("action")
def cli(action):
    """Run a Memento migration. Action can be "upgrade" to create tables or "downgrade" to destroy them."""
    alembic_cfg = config.Config(f"{CONFIG_DIR}/alembic.ini")
    alembic_cfg.set_main_option("script_location", f"{CONFIG_DIR}/migrations")

    if os.getenv(ENV_VAR, None) is None:
        rprint(
            "[red]No connection string found at environment variable:[/]",
            f"[green]{ENV_VAR}[/].",
        )
        os.environ[ENV_VAR] = Prompt.ask(
            "[bold cyan]Please enter your database connection string[/]"
        )
    else:
        rprint(f"[green]{ENV_VAR}[/] [blue]environment variable found.[/]")

    if action == "upgrade":
        command.upgrade(alembic_cfg, "head")
    elif action == "downgrade":
        command.downgrade(alembic_cfg, "base")
    else:
        raise ValueError("Invalid action.")
