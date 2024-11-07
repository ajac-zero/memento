import os

import click
from rich import print as rprint
from rich.prompt import Prompt
from sqlalchemy import create_engine

from memento.models import Base

ENV_VAR = "MEMENTO_DB_CONNECTION_STRING"


@click.command()
@click.argument("action")
@click.option("--echo/--no-echo", default=False)
def cli(action, echo):
    """Run a Memento migration. Action can be "upgrade" to create tables or "downgrade" to destroy them."""

    if action not in {"upgrade", "downgrade"}:
        raise ValueError("Invalid action. Try 'upgrade' or 'downgrade'.")

    if (db_url := os.getenv(ENV_VAR, None)) is None:
        rprint(
            "[red]No connection string found at environment variable:[/]",
            f"[green]{ENV_VAR}[/].",
        )
        db_url = Prompt.ask(
            "[bold cyan]Please enter your database connection string[/]"
        )
    else:
        rprint(f"[green]{ENV_VAR}[/] [blue]environment variable found.[/]")

    engine = create_engine(db_url, echo=echo)

    match action:
        case "upgrade":
            Base.metadata.create_all(engine)
        case "downgrade":
            Base.metadata.drop_all(engine)
