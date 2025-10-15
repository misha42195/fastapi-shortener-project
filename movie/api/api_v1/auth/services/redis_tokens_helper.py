__all__ = ("redis_tokens",)


from redis import Redis

from api.api_v1.auth.services.tokens_helper import AbstractRedisToken
from core.config import settings


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
                settings.redis.collections_names.tokens_set_name,
                token,
            ),
        )

    def get_tokens(self) -> list[str]:
        """
        получение списка токенов
        """
        return list(
            self.redis.smembers(
                settings.redis.collections_names.tokens_set_name,
            ),
        )

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
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.tokens,
    set_token=settings.redis.collections_names.tokens_set_name,
)
