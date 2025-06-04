from typing import Annotated

import typer
from rich import print
from api.api_v1.auth.services import redis_tokens
from core import config

app = typer.Typer(
    name="token",
    rich_markup_mode="rich",
    no_args_is_help=True,
    help="Tokens management.",
)


@app.command(
    name="check",
)
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


@app.command(
    name="create",
)
def create_token() -> None:
    """
    Creating a new token and saving it to the database
    """
    print(
        (
            f"[green]Create a new token[/green] [yellow]"
            f"{redis_tokens.add_token()}[yellow]"
        )
    )


@app.command(
    name="add",
)
def add_token(
    token: Annotated[
        str,
        typer.Argument(help="Add api token from console"),
    ],
) -> None:
    """
    Add the passed token to the database
    """
    redis_tokens.redis.sadd(
        config.REDIS_TOKEN_SET_NAME,
        token,
    )
    (
        print(
            f"[green]Add new token [yellow]{token}[/yellow] in database [/green]",
        )
    )


@app.command(
    name="rm",
)
def delete_token(
    token: Annotated[
        str,
        typer.Argument(help="Delete token from database"),
    ],
):
    """
    Delete token in database
    """
    if redis_tokens.token_exists(token):
        redis_tokens.delete_token(token)
        print(f"[green]Token [yellow]{token}[/yellow]delete successfully [/green]")
    else:
        print(f"[red] Token [yellow]{token}[/yellow] does not exists [/red]")
