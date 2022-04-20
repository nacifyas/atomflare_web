from config import redis

class ServiceCache():

    async def get(id: int):
        await redis.hmget(id)