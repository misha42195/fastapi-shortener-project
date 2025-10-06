import logging

from fastapi import (
    FastAPI,
)

from api import router as api_router
from api.main_views import router as hello_router
from api.redirect_views import router as redirect_router
from app_lifespan import lifespan
from core.config import settings

# настраиваем конфигурацию для логирования,
# в параметрах указываем уровень логирования, формат логирования(вид вывода сообщения)
logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
    datefmt=settings.logging.date_format,
)
app = FastAPI(
    title="Movies",
    lifespan=lifespan,
)
app.include_router(redirect_router)


app.include_router(api_router)


app.include_router(hello_router)
