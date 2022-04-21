from models.user import UserRead, ATRIBUTES_LIST
from redis.config import redis

def normalize(user_values: list[str]) -> UserRead:
    user_dict = dict(zip(ATRIBUTES_LIST, user_values))
    user_dict["id"] = int(user_dict["id"])
    user_dict["is_admin"] = bool(user_dict["is_admin"])
    return UserRead(**user_dict)

class UserCache():
    
    async def get(id: int) -> UserRead:
        return await redis.hmget(f"user:{id}", ATRIBUTES_LIST)

    async def set(user: dict) -> str:
        id = user["id"]
        await redis.delete(f"no-user:{id}")
        return await redis.hmset(f"user:{id}", user)

    async def exists(id: int) -> bool:
        return await redis.hexists(f"user:{id}") or await redis.exists(f"no-user:{id}")

    async def delete(id: int) -> int:
        return await redis.delete(f"user:{id}")

    async def set_null(id: int) -> str:
        return await redis.set(f"no-user:{id}", "None")
