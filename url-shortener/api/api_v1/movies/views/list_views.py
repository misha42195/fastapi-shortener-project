from fastapi import APIRouter
from starlette import status

from api.api_v1.movies.crud import movie_storage
from schemas.muvies import Movies, CreateMovie

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movies],
)
def movies() -> list[Movies]:
    return movie_storage.get_movies()


@router.post(
    "/",
    response_model=Movies,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_in: CreateMovie) -> Movies:
    movie = movie_storage.create_movie(
        movie_in=movie_in,
    )
    return movie
