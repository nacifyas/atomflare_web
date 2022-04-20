from models.service import Service
from redis.config import redis

def normalize():
    pass

class ServiceCache():

    async def get(id: int) -> Service:
        service = await redis.get(f"service:{id}")
        service = None if service == 'None' else service
        return service

    async def set(service: Service) -> str:
        return await redis.hmset(f"service:{service.id}", service.dict())

    async def exists(id: int) -> int:
        return await redis.exists(f"service:{id}")

    async def delete(id: int) -> int:
        return await redis.delete(f"service:{id}")

    async def set_null(id: int) -> str:
        return await redis.set(f"service:{id}","None")