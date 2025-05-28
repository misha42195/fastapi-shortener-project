from redis import Redis

from core.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
)

redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
)

if __name__ == "__main__":
    redis.set("name", "Misha")
    redis.set("age", 36)
    redis.set("foo", "bar")
    print("name", redis.get("name"))
    print("age", redis.get("age"))
    print("foo", redis.get("foo"))
    print("spam", redis.get("spam"))
    print("foo", redis.getdel("foo"))
    print("foo", redis.get("foo"))
