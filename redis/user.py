from redis.config import redis
from models.user import User

class UserCache():
    async def __init__(self) -> None:
        return await redis.execute_command(
            '''FT.CREATE user-idx ON HASH PREFIX 1 "user:" 
            SCHEMA username TEXT SORTABLE
            name TEXT SORTABLE
            is_admin TEXT
            hashed_password TEXT
            id NUMERIC SORTABLE'''
        )

    async def get_all(limit: int, skip: int) -> list[User]:
        return await redis.execute_command(f"FT.SEARCH user-idx * LIMIT {limit} {skip}")

    async def get_by_username(username: str) -> User:
        return await redis.execute_command(f"FT.SEARCH user-idx @username:{username}")
    
    async def get(id: int) -> User:
        return await redis.hmget(f"user:{id}")

    async def set(user: User) -> str:
        return await redis.hmset(f"user:{id}", **user.dict())

    async def exists(id: int) -> bool:
        return await redis.hexists(f"user:{id}")    

    async def delete(id: int) -> int:
        return await redis.delete(f"user:{id}")
