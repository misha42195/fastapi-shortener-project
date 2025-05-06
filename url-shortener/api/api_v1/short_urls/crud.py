from typing import Annotated

from fastapi import APIRouter, Depends
from api.api_v1.short_urls.dependecies import movies_list, prefetch_movie
from schemas.muvies import Movies

router = APIRouter(
    prefix="/films",
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
