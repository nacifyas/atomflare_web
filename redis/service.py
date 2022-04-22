from models.service import Service, ATRIBUTES_LIST
from redis.config import redis
import asyncio

def normalize(service_values: list[str]) -> Service:
    service_dict = dict(zip(ATRIBUTES_LIST, service_values))
    service_dict["id"] = int(service_dict["id"])
    service_dict["is_visible"] = bool(service_dict["is_visible"])
    return Service(**service_dict)

class ServiceCache():

    async def get(id: int) -> Service:
        null_service, id_service = await asyncio.gather(
            redis.get(f"no-service:{id}"),
            redis.hmget(f"service:{id}")
        )
        service = None if null_service == 'None' else normalize(id_service)
        return service

    async def set(service: dict) -> str:
        id = service["id"]
        res = await asyncio.gather (
            redis.delete(f"no-service:{id}"),
            redis.hmset(f"service:{id}", service)
        )
        return res.__str__

    async def exists(id: int) -> int:
        ex, nx = await asyncio.gather(
            redis.exists(f"service:{id}"),
            redis.exists(f"no-service:{id}")
        )
        return int(ex) + int(nx) >= 1

    async def delete(id: int) -> int:
        return await redis.delete(f"service:{id}")

    async def set_null(id: int) -> str:
        return await redis.set(f"no-service:{id}","None")
        