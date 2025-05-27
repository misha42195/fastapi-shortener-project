import logging
from typing import Annotated

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasicCredentials,
    HTTPBasic,
    HTTPBearer,
)
from fastapi import (
    HTTPException,
    BackgroundTasks,
    status,
    Request,
)
from fastapi.params import Depends

from api.api_v1.movies.crud import movie_storage
from core.config import (
    API_TOKENS,
    DB_USERNAME,
    UNSAVE_METHODS,
)
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


secrets = HTTPBasic(
    auto_error=False,
    scheme_name="Схема с полями: username, password",
    description="Объект предоставляющий поля для авторизации",
)


def user_basic_auth_required_for_unsave_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(secrets),
    ] = None,
):
    log.info("credentials %s", credentials)
    if request.method not in UNSAVE_METHODS:
        return
    if (
        credentials
        and credentials.username in DB_USERNAME
        and DB_USERNAME[credentials.username] == credentials.password
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User credentials is required. Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def validate_api_token(
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    log.info("api token %s", api_token)
    if (api_token is None) or (api_token.credentials not in API_TOKENS):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )


def validate_user_basic(
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(secrets),
    ] = None,
):
    log.info("credentials %s", credentials)

    if (
        not credentials
        or (credentials.username not in DB_USERNAME)
        or (DB_USERNAME[credentials.username] != credentials.password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token or password",
            headers={"WWW-Authenticate": "Basic"},
        )


def user_basic_or_api_token_required(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(static_api_token)
    ] = None,
    credentials: Annotated[HTTPBasicCredentials | None, Depends(secrets)] = None,
):
    if request.method not in UNSAVE_METHODS:
        return None
    if api_token:
        return validate_api_token(api_token=api_token)
    if credentials:
        return validate_user_basic(credentials=credentials)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Log in using a token or login and password",
        headers={"WWW-Authenticate": "Bearer, Basic"},
    )
