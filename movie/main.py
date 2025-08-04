import logging

from fastapi import (
    FastAPI,
)

from api import router as api_router
from api.main_views import router as hello_router
from api.redirect_views import router as redirect_router
from app_lifespan import lifespan
from core import config

# настраиваем конфигурацию для логирования,
# в параметрах указываем уровень логирования, формат логирования(вид вывода сообщения)
logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)
app = FastAPI(
    title="Movies",
    lifespan=lifespan,
)
app.include_router(redirect_router)


app.include_router(api_router)


app.include_router(hello_router)
