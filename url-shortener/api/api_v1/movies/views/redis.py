import logging
import secrets
from abc import abstractmethod, ABC

from redis import Redis

from core import config
from core.config import (
    API_TOKEN_SET_NAME,
)


class AbstractRedisToken(ABC):
    """
    - проверка наличия токена;
    - добавление токена в хранилище;
    - генерация нового токена;
    """

    @abstractmethod
    def token_exists(self, token: str) -> bool:
        pass

    @abstractmethod
    def add_token(self) -> None:
        pass

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)


class RedisToken(AbstractRedisToken):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        set_token: str,
    ):
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.token_set = set_token

    def token_exists(
        self,
        api_token: str,
    ) -> bool:
        return bool(
            self.redis.sismember(
                self.token_set,
                api_token,
            ),
        )

    def add_token(self) -> None:
        token = self.generate_token()
        self.redis.sadd(
            self.token_set,
            token,
        )


redis_token = RedisToken(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_TOKEN_DB_NUM,
    set_token=config.API_TOKEN_SET_NAME,
)
