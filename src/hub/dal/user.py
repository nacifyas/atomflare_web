from typing import Optional, Union
from sqlalchemy.orm import Session
from hub.sql.sqlmodels import UserDB
from hub.redis.user import UserCache
from hub.sql.database import async_session
from hub.models.user import User, UserCreate, UserUpdate
from sqlalchemy.future import select
from sqlalchemy import delete, update
import asyncio


def cacheNormalize(user: Union[User, UserDB]) -> dict:
    user_dict = user.dict() if isinstance(user, User) else User(**user.__dict__).dict()
    user_dict["is_admin"] = str(user.is_admin)
    user_dict.pop("hashed_password")
    return user_dict


def normalize(user: UserDB) -> Union[User, None]:
    if user is not None:
        return User(**user.__dict__)
    else:
        return None


async def begin():
    async with async_session() as session:
        async with session.begin():
            return UserDAL(session)


class UserDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all_users(self, limit: int, skip: int) -> list[Optional[User]]:
        query = await self.db_session.execute(select(UserDB).offset(skip).limit(limit))
        coro_arr = []
        user_array = []
        for user in query.scalars().all():
            user_array.append(normalize(user))
            coro_arr.append(
                UserCache.set(cacheNormalize(user))
            )
        await asyncio.gather(*coro_arr)
        return user_array

    async def get_by_username(self, username: str) -> Optional[User]:
        query = await self.db_session.execute(select(UserDB).where(UserDB.username == username))
        user = normalize(query.scalars().first())
        if user is not None:
            await UserCache.set(cacheNormalize(user))
        return user

    async def get_by_id(self, id: int) -> Optional[User]:
        user_exists, user_retrieval = await asyncio.gather(
            UserCache.exists(id),
            UserCache.get(id)
        )
        if user_exists:
            return user_retrieval
        else:
            query = await self.db_session.execute(select(UserDB).where(UserDB.id == id))
            user = normalize(query.scalars().first())
            if user is not None:
                await UserCache.set(cacheNormalize(user))
            else:
                await UserCache.set_null(id)
            return user

    async def create_user(self, user: UserCreate) -> Optional[User]:
        new_user = UserDB(**user.dict())
        self.db_session.add(new_user)
        await self.db_session.flush()
        await UserCache.set(cacheNormalize(new_user))
        new_user_norm = normalize(new_user)
        return new_user_norm

    async def update_user(self, user: UserUpdate) -> Optional[User]:
        old_user = await self.get_by_id(user.id)
        if old_user is not None:
            query = update(UserDB).where(UserDB.id == user.id)
            if user.name:
                query = query.values(name=user.name)
                old_user.name = user.name
            if user.username:
                query = query.values(username=user.username)
                old_user.username = user.username
            if user.hashed_password:
                query = query.values(hashed_password=user.hashed_password)
                old_user.hashed_password = user.hashed_password
            if user.is_admin is not None:
                query = query.values(is_admin=user.is_admin)
                old_user.is_admin = user.is_admin
            query.execution_options(synchronize_session="fetch")
            await self.db_session.execute(query)
            await UserCache.set(cacheNormalize(old_user))
            return old_user
        else:
            await UserCache.set_null(user.id)
            return None

    async def delete_user(self, id: int) -> None:
        query = delete(UserDB).where(UserDB.id == id)
        query.execution_options(synchronize_session="fetch")
        await asyncio.gather(
            self.db_session.execute(query),
            UserCache.delete(id),
            UserCache.set_null(id)
        )
