from fastapi import (
    APIRouter,
)
from starlette import status

from dependencies.movies import (
    GetMovieStorage,
    MovieBySlug,
)
from schemas.muvies import (
    Movies,
    MoviesPartialUpdate,
    MoviesRead,
    UpdateMovies,
)

router = APIRouter(
    prefix="/{slug}",
    tags=["Movies"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movies not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie 'lost' not found",
                    },
                },
            },
        },
    },
)


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
    movie: MovieBySlug,
    movie_data_in: UpdateMovies,
    storage: GetMovieStorage,
) -> Movies:
    return storage.update_movie(
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
    storage: GetMovieStorage,
) -> Movies:
    return storage.movie_partial_update(
        movies=movie,
        movies_in=movie_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: MovieBySlug,
    storage: GetMovieStorage,
) -> None:
    storage.delete(movie)


@router.post(
    "/transfer_movie/",
)
def transfer_movie() -> dict[str, str]:
    # raise NotImplementedError
    return {"status": "200"}
