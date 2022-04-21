from models.service import Service, ATRIBUTES_LIST
from redis.config import redis

def normalize(service_values: list[str]) -> Service:
    service_dict = dict(zip(ATRIBUTES_LIST, service_values))
    service_dict["id"] = int(service_dict["id"])
    service_dict["is_visible"] = bool(service_dict["is_visible"])
    return Service(**service_dict)

class ServiceCache():

    async def get(id: int) -> Service:
        service = await redis.get(f"no-service:{id}")
        service = None if service == 'None' else normalize(await redis.hmget(f"service:{id}", ATRIBUTES_LIST))
        return service

    async def set(service: dict) -> str:
        id = service["id"]
        await redis.delete(f"no-service:{id}")
        return await redis.hmset(f"service:{id}", service)

    async def exists(id: int) -> int:
        return await redis.exists(f"service:{id}") or await redis.exists(f"no-service:{id}")

    async def delete(id: int) -> int:
        return await redis.delete(f"service:{id}")

    async def set_null(id: int) -> str:
        return await redis.set(f"no-service:{id}","None")
        