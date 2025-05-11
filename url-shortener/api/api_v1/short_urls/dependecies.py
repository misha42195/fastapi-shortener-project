from datetime import date

from fastapi import HTTPException
from starlette import status

from api.api_v1.short_urls.crud import movie_storage
from schemas.muvies import Movies
from schemas.short_url import ShortenedUrl


# def prefetch_short_url(slug: str) -> ShortenedUrl:
#     url: ShortenedUrl | None = short_url_storage.get_by_slug(slug=slug)
#     if url:
#         return url
#
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"URL {slug!r} not found",
#     )


def prefetch_movie(slug: str) -> Movies:
    movie: Movies | None = movie_storage.get_by_slug(
        slug=slug,
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {slug!r} not found",
    )
