__all__ = ("UNSAVE_METHODS",)
import logging
from pathlib import Path
from typing import Self

from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BaseDir = Path(__file__).resolve().parent  # получаем путь до папки с файлом movie.json

PATH_TO_MOVIE_FILE = BaseDir / "movies_data.json"  # полный путь до директории movie


LOG_LEVEL: int = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
UNSAVE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    },
)


class LoggingConfig(BaseSettings):
    log_level: int = LOG_LEVEL
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"


# подкласс для установки значений пол
class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisDatabaseConfig(BaseModel):
    default: int = 0
    tokens: int = 1
    users: int = 2
    movies: int = 3

    @model_validator(mode="after")
    def validate_dbs_numbers_unique(self) -> Self:
        db_values = list(self.model_dump().values())
        if len(set(db_values)) != len(db_values):
            raise ValueError("Database numbers must should be unique")
        return self


class RedisCollectionsNamesConfig(BaseModel):
    tokens_set_name: str = "tokens"
    users_set_name: str = "users"
    movies_hash_name: str = "movies"


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDatabaseConfig = RedisDatabaseConfig()
    collections_names: RedisCollectionsNamesConfig = RedisCollectionsNamesConfig()


# базовый класс по объекту которого получаем настройки
# атрибутами объекта будут другие объекты настройки
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(
            BaseDir / ".env.template",
            BaseDir / ".env",
        ),
        env_prefix="MOVIE__",
        env_nested_delimiter="__",
    )
    redis: RedisConfig = RedisConfig()
    logging: LoggingConfig = LoggingConfig()


settings = Settings()
