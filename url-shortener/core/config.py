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
API_TOKENS = frozenset(
    {
        "kCfNDf_FYwzLlZHj8v7oZvk0O8k",
        "igcGEPmVXNQC8tTdUCDKsPzDFWc",
        "FOhbQbqnIF8xIe7HXgQvXwFp1Lg",
    }
)

DB_USERNAME: dict[str, str] = {
    # username: password
    "bob": "1234",
    "sem": "qwerty",
}
