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
    HTTPBasicCredentials,
    HTTPBearer,
)

from dependencies.auth import (
    UNSAVE_METHODS,
    username_basic_auth,
    validate_basic_auth,
)
from dependencies.movies import GetMovieStorage
from schemas.muvies import Movies
from services.auth.redis_tokens_helper import redis_tokens

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


def user_basic_or_api_token_required(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(username_basic_auth),
    ] = None,
) -> None:
    if request.method not in UNSAVE_METHODS:
        return None
    if api_token:
        return validate_api_token(api_token=api_token)
    if credentials:
        return validate_basic_auth(credentials=credentials)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Log in using a token or login and password",
        headers={"WWW-Authenticate": "Bearer, Basic"},
    )
