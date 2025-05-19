from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from api.api_v1.movies.crud import movie_storage
from api.api_v1.movies.dependecies import save_storage_state

from schemas.muvies import (
    Movies,
    CreateMovies,
    MoviesRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[
        Depends(save_storage_state),
    ],
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
) -> Movies:
    return movie_storage.create_movie(movie_in=movie_in)
