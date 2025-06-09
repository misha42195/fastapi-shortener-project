from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # выполняем код до запуска основного приложения
    # приложение ставим на паузу на время его выполнения
    yield
    # выполняем завершение работы, закрываем соединения
    # финально сохраняем проект
