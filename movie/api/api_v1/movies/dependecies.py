import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    Request,
    status,
)
from fastapi.params import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)

from api.api_v1.auth.services.redis_tokens_helper import redis_tokens
from api.api_v1.auth.services.redis_users_helper import redis_users
from core.config import (
    UNSAVE_METHODS,
)
from dependencies.movies import GetMovieStorage
from schemas.muvies import Movies

log = logging.getLogger(__name__)


def prefetch_movie(
    slug: str,
    movie_storage: GetMovieStorage,
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


static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **api token** for developer portal [read more](#) ",
    auto_error=False,
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
) -> None:
    log.info("credentials %s", credentials)
    if request.method not in UNSAVE_METHODS:
        return
    # Проверить пароль через Redis
    if credentials and redis_users.validate_password_match(
        credentials.username,
        credentials.password,
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
) -> None:
    log.info("api token %s", api_token)
    if api_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API token",
        )
    if redis_tokens.token_exists(api_token.credentials):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


def validate_user_basic(
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(secrets),
    ] = None,
) -> None:
    log.info("credentials %s", credentials)

    if credentials and redis_users.validate_password_match(
        credentials.username,
        credentials.password,
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_or_api_token_required(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(secrets),
    ] = None,
) -> None:
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
