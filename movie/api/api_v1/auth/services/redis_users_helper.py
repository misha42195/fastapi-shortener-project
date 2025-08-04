from typing import cast

from redis import Redis

from api.api_v1.auth.services.users_helper import AbstractUsersHelper
from core import config


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
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db_num=config.REDIS_USER_DB_NUM,
    set_name=config.REDIS_USER_SET_NAME,
)
