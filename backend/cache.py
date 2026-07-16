import json
import os

import redis
from dotenv import load_dotenv

load_dotenv()


redis_client = redis.Redis.from_url(
    os.getenv("REDIS_BROKER_URL","redis://localhost:6379/0"),decode_responses=True)

def get_cache(key):
    try:
        data = redis_client.get(key)
        if data is None:
            return None
        return json.loads(data)
    except redis.RedisError:
        return None

def set_cache(key, data, expiry=3600):
    try:
        redis_client.setex(key,expiry,json.dumps(data),)

    except redis.RedisError:
        pass


def delete_cache(key):
    try:
        redis_client.delete(key)

    except redis.RedisError:
        pass


def delete_cache_pattern(pattern):
    try:
        keys = list(redis_client.scan_iter(match=pattern)
)
        if keys:
            redis_client.delete(*keys)
    except redis.RedisError:
        pass