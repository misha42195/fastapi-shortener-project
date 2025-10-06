from redis import Redis

from core.config import settings

redis = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.default,
    decode_responses=True,
)

if __name__ == "__main__":
    print(redis.ping())
    redis.set("name", "Misha")
    redis.set("age", 36)
    redis.set("foo", "bar")
    print("foo", redis.get("foo"))
    print("spam", redis.get("spam"))
    print("spam", redis.get("spam"))
