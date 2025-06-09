__all__ = ("app",)

import typer

from commands.hello import app as hello_app
from commands.token import app as check_app

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.callback()
def callback() -> None:
    """
    Some CLI management command
    """


app.add_typer(hello_app)
app.add_typer(check_app)
