import logging
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
# tokens for testing
# 1) "idV8XTAfbS2JOh7690mHlA"
# 2) "bsXxwPUJ6jo26PAK3mPG9g"
# 3) "HKieZrytophWYQWVlQ3Z2g"


DB_USERNAME: dict[str, str] = {
    # username: password
    "bob": "1234",
    "sem": "qwerty",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
# REDIS_DB_NUM = 0
REDIS_TOKEN_DB_NUM = 1

API_TOKEN_SET_NAME = "tokens"
