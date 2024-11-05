import os
import click
from rich import print
from rich.prompt import Prompt


@click.command()
def cli():
    db_url = os.getenv("MEMENTO_DB_URL", None)

    if db_url is None:
        print("No connection string found at environment variable `MEMENTO_DB_URL`.")
        db_url = Prompt.ask("Enter your database connection string")

    print(db_url)


if __name__ == "__main__":
    cli()
