from typing import cast

from redis import Redis

from core.config import settings
from services.auth.users_helper import AbstractUsersHelper


class RedisUsersHelper(AbstractUsersHelper):
    def __init__(
        self,
        host: str,
        port: str | int | None,
        db_num: int,
        set_name: str,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db_num,
            decode_responses=True,
        )
        self.set_name = set_name

    def get_user_password(self, username: str) -> str | None:
        return cast(str, self.redis.get(username))


redis_users = RedisUsersHelper(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db_num=settings.redis.db.users,
    set_name=settings.redis.collections_names.users_set_name,
)
