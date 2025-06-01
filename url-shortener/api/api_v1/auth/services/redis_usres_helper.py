from redis import Redis
from api.api_v1.auth.services.users_helper import AbstractUserHelper
from core import config


class UsersAuth(AbstractUserHelper):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        set_name: str,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.set_name = set_name

    # получаем пароль пользователя из базы
    def get_user_password(self, username: str) -> str | None:
        return self.redis.get(username)


redis_user_auth = UsersAuth(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_USER_DB_NUM,
    set_name=config.API_USER_SET_NAME,
)
