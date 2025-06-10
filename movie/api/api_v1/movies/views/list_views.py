from fastapi import (
    APIRouter,
    HTTPException,
)
from fastapi.params import Depends
from starlette import status

from api.api_v1.movies.crud import (
    MovieAlreadyExistsError,
    movie_storage,
)
from api.api_v1.movies.dependecies import (
    user_basic_or_api_token_required,
)
from schemas.muvies import (
    CreateMovies,
    Movies,
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
    },
)


@router.get(
    "/",
    # response_model=list[Movies],
)
def movies() -> list[Movies]:
    return movie_storage.get_movies()


@router.post(
    "/",
    response_model=MoviesRead,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Such an object already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug='foobar' already exists.",
                    }
                }
            },
        }
    },
)
def create_movie(
    movie_in: CreateMovies,
) -> HTTPException:

    try:
        return movie_storage.create_raise_already_exists(movie_in)
    except MovieAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Movie with slug={movie_in.slug!r} already exists.",
        )
