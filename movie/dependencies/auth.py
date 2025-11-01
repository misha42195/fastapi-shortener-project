import logging
from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
)
from starlette import status
from starlette.requests import Request

from services.auth.redis_users_helper import redis_users

log = logging.getLogger(__name__)

UNSAVE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    },
)
user_basic_auth = HTTPBasic(
    auto_error=False,
    scheme_name="Схема с полями: username, password",
    description="Объект предоставляющий поля для авторизации",
)


def validate_basic_auth(
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
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


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
) -> None:
    if request.method not in UNSAVE_METHODS:
        return

    validate_basic_auth(
        credentials=credentials,
    )
