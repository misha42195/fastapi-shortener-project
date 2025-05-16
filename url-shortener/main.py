import logging

from fastapi import (
    FastAPI,
)
from starlette.requests import Request
from api import router as api_router
from api.redirect_views import router as redirect_router
from app_lifespan import lifespan
from core import config

app = FastAPI(
    title="Movies",
    lifespan=lifespan,
)
app.include_router(api_router)
app.include_router(redirect_router)

# настраиваем конфигурацию для логирования,
# в параметрах указываем уровень логирования, формат логирования(вид вывода сообщения)
logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)


@app.get("/")
def get_root(request: Request, name: str = "World"):
    docs_path = str(
        request.url.replace(
            path="/docs",
            query="",
        )
    )

    return {
        "message": f"Hello {name}",
        "docs_path": docs_path,
    }
