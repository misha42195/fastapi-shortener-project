__all__ = ("redis_tokens",)


from redis import Redis

from api.api_v1.auth.services.tokens_helper import AbstractRedisToken
from core import config


class RedisToken(AbstractRedisToken):

    def __init__(
        self,
        host: str,
        port: str | int | None,
        db: int,
        set_token: str,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.token_set = set_token

    def delete_token(self, token: str) -> bool:
        return bool(
            self.redis.srem(
                config.REDIS_TOKEN_SET_NAME,
                token,
            )
        )

    def get_tokens(self) -> list[str]:
        """
        получение списка токенов
        """
        return list(self.redis.smembers(config.REDIS_TOKEN_SET_NAME))

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

    def add_token(self) -> str:
        token: str = self.generate_token()
        self.redis.sadd(
            self.token_set,
            token,
        )
        return token


redis_tokens = RedisToken(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_TOKEN_DB_NUM,
    set_token=config.REDIS_TOKEN_SET_NAME,
)
