__all__ = (
    "DB_USERNAME",
    "UNSAVE_METHODS",
)
import logging
from os import getenv
from pathlib import Path

BaseDir = Path(__file__).resolve().parent  # получаем путь до папки с файлом movie.json

PATH_TO_MOVIE_FILE = (
    BaseDir / "movies_data.json"
)  # полный путь до файла для записи данных


LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
UNSAVE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


DB_USERNAME: dict[str, str] = {
    # username: password
    "bob": "1234",
    "sem": "qwerty",
}

REDIS_HOST = "localhost"

REDIS_PORT = getenv("REDIS_PORT") if getenv("REDIS_PORT") else 6379

REDIS_DB_NUM = 1

REDIS_TOKEN_DB_NUM = 1

REDIS_USER_DB_NUM = 2

REDIS_MOVIES_DB_NUM = 3

REDIS_TOKEN_SET_NAME = "tokens"

REDIS_USER_SET_NAME = "users"

REDIS_MOVIES_SET_NAME = "movies"
