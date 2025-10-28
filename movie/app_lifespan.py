from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from storage.movies import MoviesStorage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.movie_storage = MoviesStorage(
        hash_name=settings.redis.collections_names.movies_hash_name,
    )
    yield
