from fastapi import (
    APIRouter,
    HTTPException,
)
from fastapi.params import Depends
from starlette import status

from api.api_v1.movies.dependecies import (
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from dependencies.movies import GetMovieStorage
from schemas.muvies import (
    CreateMovies,
    Movies,
    MoviesRead,
)
from storage.movies.exeptions import MovieAlreadyExistsError

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
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
    },
)


@router.get(
    "/",
    # response_model=list[Movies],
)
def movies(
    storage: GetMovieStorage,
) -> list[Movies]:
    return storage.get_movies()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Such an object already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug='foobar' already exists.",
                    },
                },
            },
        },
    },
)
def create_movie(
    movie_in: CreateMovies,
    storage: GetMovieStorage,
) -> MoviesRead:
    try:
        return storage.create_raise_already_exists(movie_in)  # type: ignore
    except MovieAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Movie with slug={movie_in.slug!r} already exists.",
        )
