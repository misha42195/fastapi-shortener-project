from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from core.config import settings
from services.auth import redis_tokens

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
) -> None:
    """
    Check if the passed token is valid - exist or not
    """
    print(
        (
            f"API token [bold][yellow]{token}[/yellow][/bold] [green]exists[/green]"
            if redis_tokens.token_exists(token)
            else f"Token [bold][yellow]{token}[/yellow][/bold][red] doesnt exist[/red]"
        ),
    )


@app.command(
    name="list",
)
def list_tokens() -> None:  # имя команды
    """
    List all tokens
    """
    (
        print(
            Markdown(
                "# Список токенов\n\n"
                + "\n".join([f"- {token}" for token in redis_tokens.get_tokens()]),
            ),
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
        ),
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
        settings.redis.collections_names.tokens_set_name,
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
) -> None:
    """
    Delete token in database
    """
    if redis_tokens.token_exists(token):
        redis_tokens.delete_token(token)
        print(f"[green]Token [yellow]{token}[/yellow] delete successfully [/green]")
        return
    print(f"[red] Token [yellow]{token}[/yellow] does not exists [/red]")
