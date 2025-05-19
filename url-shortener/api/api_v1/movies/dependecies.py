from fastapi import HTTPException, BackgroundTasks
from starlette import status
import logging

from starlette.requests import Request

from api.api_v1.movies.crud import movie_storage
from schemas.muvies import Movies

log = logging.getLogger(__name__)


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


UNSAVE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


def save_storage_state(
    background_tasks: BackgroundTasks,
    method: Request,
):
    # до входа в представление view
    log.info("Метод запроса %r ", method.method)
    yield
    # после выхода из представления
    if method.method in UNSAVE_METHODS:
        log.info("Добавление фоновой задачи. Сохранение состояния")
        background_tasks.add_task(movie_storage.save_movie)
