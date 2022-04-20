import aioredis

SECRET="0fngsCHvum0opzdWbxnehlMZgTKFydH7"
REDIS_PATH="redis://redis-13736.c293.eu-central-1-1.ec2.cloud.redislabs.com:13736" 
ENCODING="utf-8"

redis = aioredis.from_url(url=REDIS_PATH, password=SECRET, encoding=ENCODING, decode_responses=True)