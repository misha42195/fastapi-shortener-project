__all__ = ("app",)

import typer

from commands.hello import app as hello_app
from commands.token import app as check_app
from commands.lists import app as tokens_app


app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.callback()
def callback():
    """
    Some CLI management command
    """


app.add_typer(hello_app)
app.add_typer(check_app)
app.add_typer(tokens_app)
