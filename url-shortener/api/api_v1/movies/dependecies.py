import logging
from typing import Annotated

from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException, BackgroundTasks
from fastapi.security import HTTPBearer
from fastapi.params import Depends
from starlette import status
from starlette.requests import Request

from api.api_v1.movies.crud import movie_storage
from core.config import API_TOKENS
from schemas.muvies import Movies

log = logging.getLogger(__name__)


def prefetch_movie(
    slug: str,
) -> Movies:
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


static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **api token** for developer portal [read more](#) ",
    auto_error=False,
)


def required_api_token_for_unsave_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    log.info("API token %s", api_token)
    if request.method not in UNSAVE_METHODS:
        return

    if api_token.credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect api-token",
        )
