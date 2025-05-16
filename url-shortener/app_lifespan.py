from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.api_v1.movies.crud import movie_storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    # выполняем код до запуска основного приложения
    # приложение ставим на паузу на время его выполнения
    movie_storage.init_storage_from_state()
    yield
    # выполняем завершение работы, закрываем соединения
    # финально сохраняем проект
