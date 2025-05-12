from fastapi import HTTPException
from starlette import status

from api.api_v1.movies.crud import movie_storage
from schemas.muvies import Movies


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
