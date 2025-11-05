from typing import Annotated, cast

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.requests import Request
from starlette import status

from schemas.muvies import Movies
from storage.movies import MoviesStorage


def get_movie_storage(
    request: Request,
) -> MoviesStorage:
    return cast(MoviesStorage, request.app.state.movie_storage)


GetMovieStorage = Annotated[
    MoviesStorage,
    Depends(get_movie_storage),
]


def prefetch_movie(
    slug: str,
    movie_storage: GetMovieStorage,
) -> Movies:
    movie: Movies | None = movie_storage.get_by_slug(
        slug=slug,
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {slug!r} not found",
    )


MovieBySlug = Annotated[
    Movies,
    Depends(prefetch_movie),
]
