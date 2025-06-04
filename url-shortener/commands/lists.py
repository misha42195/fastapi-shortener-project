import typer

from rich import print
from rich.markdown import Markdown
from api.api_v1.auth.services import redis_tokens

app = typer.Typer(
    name="tokens",  # имя команды
    rich_markup_mode="rich",
    help="All tokens in base",
)


@app.command(
    name="list",
)
def list_tokens():  # имя команды
    """
    List all tokens
    """
    (
        print(
            Markdown(
                "# Список токенов\n\n"
                + "\n".join([f"- {token}" for token in redis_tokens.get_tokens()])
            )
        )
    )
