import aioredis

REDIS_PATH = "redis://192.168.0.57:6380"
ENCODING = "utf-8"

redis = aioredis.from_url(
    url=REDIS_PATH,
    encoding=ENCODING,
    decode_responses=True
    )
