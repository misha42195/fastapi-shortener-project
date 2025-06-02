from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from api.api_v1.movies.crud import movie_storage, redis_movies
from api.api_v1.movies.dependecies import (
    user_basic_or_api_token_required,
)

from schemas.muvies import (
    Movies,
    CreateMovies,
    MoviesRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[
        Depends(user_basic_or_api_token_required),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "This movie already exists in the database.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug='foobar' already exists.",
                    }
                }
            },
        },
    },
)


@router.get(
    "/",
    response_model=list[Movies],
)
def movies() -> list[Movies]:
    return movie_storage.get_movies()


@router.post(
    "/",
    response_model=MoviesRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_in: CreateMovies,
) -> HTTPException | Any:
    if not movie_storage.get_by_slug(movie_in.slug):
        return movie_storage.create_movie(
            movie_in=movie_in,
        )
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Movie with slug={movie_in.slug!r} already exists.",
    )
