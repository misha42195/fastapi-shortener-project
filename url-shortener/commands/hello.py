from typing import Annotated

import typer
from rich import print

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command(help="Great user by name.")
def hello(
    name: Annotated[
        str,
        typer.Argument(help="Name to greet"),
    ],
):
    print(f"Hello, [bold][red]{name}[/red][/bold]")
