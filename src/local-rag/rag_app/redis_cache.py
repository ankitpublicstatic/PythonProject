import redis
import json
import hashlib

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def cache_key(query):
    return hashlib.md5(query.encode()).hexdigest()

def get_cache(query):
    key = cache_key(query)
    value = r.get(key)
    if value:
        return json.loads(value)
    return None

# def set_cache(query, response):
#     key = cache_key(query)
#     r.setex(key, 3600, json.dumps(response))  # 1 hour TTL

def set_cache(query, response):
    key = cache_key(query)
    if isinstance(response, str):
        r.setex(key, 3600, response)
    else:
        r.setex(key, 3600, json.dumps(response))