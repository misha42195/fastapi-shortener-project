from typing import Annotated, cast

from fastapi import Depends
from fastapi.requests import Request

from storage.movies import MoviesStorage


def get_movie_storage(
    request: Request,
) -> MoviesStorage:
    return cast(MoviesStorage, request.app.state.movie_storage)


GetMovieStorage = Annotated[
    MoviesStorage,
    Depends(get_movie_storage),
]
