from datetime import date, datetime
from typing import Any

from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from core.config import BASE_DIR


def inject_data_and_now(request: Request) -> dict[str, Any]:
    return {
        "today": date.today(),  # вернёт сегодняшнюю дату
        "now": datetime.now(),  # вернёт текущие дату и время
    }


templates = Jinja2Templates(
    directory=BASE_DIR / "templates",  # путь до папки с шаблонами
    context_processors=[
        inject_data_and_now,
    ],
)
