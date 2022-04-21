from models.service import Service, ATRIBUTES_LIST
from redis.config import redis

def normalize(list: list[str]) -> Service:
    return Service(**dict(zip(ATRIBUTES_LIST, list)))


class ServiceCache():

    async def get(id: int) -> Service:
        service = await redis.get(f"no-such-service:{id}")
        service = None if service == 'None' else normalize(await redis.hmget(f"service:{id}", ATRIBUTES_LIST))
        return service

    async def delete(id: int) -> int:
        return await redis.delete(f"service:{id}")

    async def set(service: Service) -> str:
        await redis.delete(f"no-such-service:{id}")
        return await redis.hmset(f"service:{service.id}", service.to_dict())

    async def exists(id: int) -> int:
        return await redis.exists(f"service:{id}") or await redis.exists(f"no-such-service:{id}")

    async def set_null(id: int) -> str:
        return await redis.set(f"no-such-service:{id}","None")