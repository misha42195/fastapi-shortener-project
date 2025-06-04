import typer
from rich.console import Console
from rich import print
from rich.markdown import Markdown
from api.api_v1.auth.services import redis_tokens

app = typer.Typer(
    name="tokens",  # имя команды
    rich_markup_mode="rich",
    help="All tokens in base",
)


@app.command()
def lists():  # имя команды
    console = Console()
    markdown_text = "# Список токенов\n\n" + "\n".join(
        [f"- {token}" for token in redis_tokens.get_tokens()]
    )

    console.print(Markdown(markdown_text))
