from typing import Annotated

from fastapi import APIRouter
from fastapi import status
from fastapi.params import Depends

from api.api_v1.short_urls.crud import movie_storage
from schemas.muvies import Movies, CreateMovie
from api.api_v1.short_urls.dependecies import prefetch_movie

router = APIRouter(
    prefix="/movie",
    tags=["Movies"],
)

#
# @router.get(
#     "/",
#     response_model=list[ShortenedUrl],
# )
# def read_short_url() -> list[ShortenedUrl]:
#     return short_url_storage.get()
#
#
# @router.get(
#     "/{slug}",
#     response_model=ShortenedUrl,
# )
# def read_short_url_details(
#     url: Annotated[
#         ShortenedUrl,
#         Depends(prefetch_short_url),
#     ],
# ) -> ShortenedUrl:
#     return url
#
#
# @router.post(
#     "/",
#     response_model=ShortenedUrl,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_short_url(short_url: ShortenedUrlCreated) -> ShortenedUrl:
#     return ShortenedUrl(
#         **short_url.model_dump(),
#     )


@router.get(
    "/",
    response_model=list[Movies],
)
def movies() -> list[Movies]:
    return movie_storage.get_movies()


@router.get(
    "/{slug}/",
    response_model=Movies,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie 'ввв' not found",
                    },
                },
            },
        }
    },
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
def create_movie(movie_in: CreateMovie) -> Movies:
    movie = movie_storage.create_movie(
        movie_in=movie_in,
    )
    return movie


@router.delete(
    "/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie 'ввв' not found",
                    },
                },
            },
        }
    },
)
def delete_movie(
    movie: Annotated[Movies, Depends(prefetch_movie)],
):
    movie_storage.delete(movie)
