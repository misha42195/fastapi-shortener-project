from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from api.api_v1.movies.crud import movie_storage
from api.api_v1.movies.dependecies import prefetch_movie
from schemas.muvies import (
    Movies,
    UpdateMovie,
)

router = APIRouter(
    prefix="/slug",
    tags=["Movies"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movies not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie 'bbb' not found",
                    },
                },
            },
        },
    },
)


@router.get(
    "/",
    response_model=Movies,
)
def get_movie(
    movie: Annotated[
        Movies,
        Depends(prefetch_movie),
    ],
) -> Movies:

    return movie


MovieBySlug = Annotated[
    Movies,
    Depends(prefetch_movie),
]


@router.put(
    "/",
    response_model=Movies,
)
def update_movie_details(
    movie: MovieBySlug,
    movie_data_in: UpdateMovie,
):
    movie = movie_storage.update_movie(movie, movie_data_in)
    return movie


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: MovieBySlug,
):
    movie_storage.delete(movie)
