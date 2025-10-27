# cache-aside-w-redis/redis_cache.py
import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB


def get_redis_connection():
    try:
        r = redis.StrictRedis(
            host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
        )
        r.ping()
        print("✅ Redis connected!")
        return r
    except redis.exceptions.ConnectionError as error:
        print("\n" + "=" * 50)
        print("🚨 Error when connecting with REDIS 🚨")
        print(f"Check if the Redis is running.")
        print(f"Details: {error}")
        print("=" * 50 + "\n")
        return None


def test_redis():
    r = get_redis_connection()
    if r:
        r.set("test_key", "Hello Redis!")
        value = r.get("test_key")
        r.delete("test_key")
        print(f"[REDIS TEST] Key 'test_key' set and read successfully. Value: {value}")
        return r
    return None


if __name__ == "__main__":
    test_redis()
