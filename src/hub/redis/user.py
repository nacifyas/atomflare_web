from typing import Optional
from hub.models.user import UserRead, ATRIBUTES_LIST
from hub.redis.config import redis
import asyncio


def normalize(user_values: list[str]) -> Optional[UserRead]:
    if user_values == [None]*len(user_values):
        return None
    else:
        user_dict = dict(zip(ATRIBUTES_LIST, user_values))
        user_dict["id"] = int(user_dict["id"])
        user_dict["is_admin"] = bool(user_dict["is_admin"])
        return UserRead(**user_dict)


class UserCache:
    async def get(self, id: int) -> Optional[UserRead]:
        null_user, id_user = await asyncio.gather(
            redis.get(f"no-user:{id}"),
            redis.hmget(f"user:{id}", ATRIBUTES_LIST)
        )
        user = None if null_user == 'None' else normalize(id_user)
        return user

    async def set(self, user: dict) -> str:
        id = user["id"]
        res = await asyncio.gather(
            redis.delete(f"no-user:{id}"),
            redis.hmset(f"user:{id}", user)
        )
        return res.__str__

    async def exists(self, id: int) -> int:
        ex, nx = await asyncio.gather(
            redis.exists(f"user:{id}"),
            redis.exists(f"no-user:{id}")
        )
        return int(ex) + int(nx) >= 1

    async def delete(self, id: int) -> int:
        return await redis.delete(f"user:{id}")

    async def set_null(self, id: int) -> str:
        return await redis.set(f"no-user:{id}", "None")
