import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from services.auth.redis_users_helper import redis_users
from starlette import status

log = logging.getLogger(__name__)

user_basic_auth = HTTPBasic(
    auto_error=False,
    scheme_name="Схема с полями: username, password",
    description="Объект предоставляющий поля для авторизации",
)

UNSAVE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    },
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
