from redis import Redis

from core import config

redis_token = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_TOKEN_DB_NUM,
)
