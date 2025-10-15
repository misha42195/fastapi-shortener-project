__all__ = ("GetMovieStorage",)
from typing import Annotated

from fastapi import Depends

from core.config import settings
from storage.movies import MoviesStorage


def get_movie_storage() -> MoviesStorage:
    return MoviesStorage(
        hash_name=settings.redis.collections_names.movies_hash_name,
    )


GetMovieStorage = Annotated[
    MoviesStorage,
    Depends(get_movie_storage),
]
