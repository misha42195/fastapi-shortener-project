import random
from datetime import date
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
    Form,
)
from api.api_v1.short_urls.dependecies import movies_list, prefetch_movie
from schemas.muvies import (
    Movies,
    CreateMovie,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movies],
)
def get_movies():
    return movies_list


@router.get(
    "/{movie_id}/",
    response_model=Movies,
)
def get_movie(
    movie: Annotated[
        Movies,
        Depends(prefetch_movie),
    ],
) -> Movies:
    return movie


@router.post(
    "/",
    response_model=Movies,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movies: CreateMovie) -> Movies:

    movie_id = random.randint(0, 100)
    return Movies(
        id=movie_id,
        **movies.model_dump(),
    )
