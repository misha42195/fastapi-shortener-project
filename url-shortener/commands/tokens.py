from typing import Annotated

import typer
from rich import print
from api.api_v1.auth.services import redis_tokens

app = typer.Typer(
    name="token",
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Tokens management.",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(help="Chek api token"),
    ],
):
    """
    Check if the passed token is valid - exist or not
    """
    print(
        (
            f"API token [bold][yellow]{token}[/yellow][/bold] [green]exists[/green]"
            if redis_tokens.token_exists(token)
            else f"Token [bold][yellow]{token}[/yellow][/bold][red] doesnt exist[/red]"
        )
    )
