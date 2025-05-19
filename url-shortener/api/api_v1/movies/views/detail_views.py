from typing import Annotated

from fastapi import (
    APIRouter,
)
from fastapi.params import Depends
from starlette import status

from api.api_v1.movies.crud import movie_storage
from api.api_v1.movies.dependecies import prefetch_movie, save_storage_state
from schemas.muvies import (
    Movies,
    UpdateMovies,
    MoviesPartialUpdate,
    MoviesRead,
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

MovieBySlug = Annotated[
    Movies,
    Depends(prefetch_movie),
]


@router.get(
    "/",
    response_model=MoviesRead,
)
def get_movie(
    movie: MovieBySlug,
) -> Movies:

    return movie


@router.put(
    "/",
    response_model=MoviesRead,
)
def update_movie_details(
    movie: MovieBySlug, movie_data_in: UpdateMovies, _=Depends(save_storage_state)
):
    return movie_storage.update_movie(
        movie=movie,
        movie_data_in=movie_data_in,
    )


@router.patch(
    "/",
    response_model=MoviesRead,
)
def update_movie_detail_partial(
    movie: MovieBySlug,
    movie_in: MoviesPartialUpdate,
):
    return movie_storage.movie_partial_update(
        movies=movie,
        movies_in=movie_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: MovieBySlug,
):
    movie_storage.delete(movie)
