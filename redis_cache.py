import redis
import json
import decimal
from config import REDIS_HOST, REDIS_PORT, REDIS_DB, CACHE_TTL


def decimal_default_encoder(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError


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


r = get_redis_connection()


def test_redis():
    if r:
        r.set(
            "test_key",
            "Hello Redis!",
        )
        value = r.get("test_key")
        r.delete("test_key")
        print(f"[REDIS TEST] Key 'test_key' set and read successfully. Value: {value}")
        return r
    return None


def get_from_cache(key: str) -> dict or None:
    if not r:
        return None

    data_json = r.get(key)
    if data_json:
        return json.loads(data_json)

    return None


def set_in_cache(key: str, data: dict, ttl: int = CACHE_TTL):
    if not r:
        return

    data_json = json.dumps(data, default=decimal_default_encoder)
    r.setex(key, ttl, data_json)


if __name__ == "__main__":
    test_redis()
