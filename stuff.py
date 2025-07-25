from redis import Redis

from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_NUM,
    decode_responses=True,
)

if __name__ == "__main__":
    print(redis.ping())
    redis.set("name", "Misha")
    redis.set("age", 36)
    redis.set("foo", "bar")
    print("name", redis.get("name"))
    print("age", redis.get("age"))
    print("foo", redis.get("foo"))
    print("spam", redis.get("spam"))
    print("foo", redis.getdel("foo"))
    print("foo", redis.get("foo"))
