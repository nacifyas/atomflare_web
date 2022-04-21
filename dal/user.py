from sqlalchemy.orm import Session
from sql.sqlmodels import UserDB
from redis.user import UserCache
from models.user import User, UserCreate, UserUpdate
from sqlalchemy.future import select
from sqlalchemy import delete, update

def cacheNormalize(user: User) -> dict:
    user_dict = user.dict()
    user_dict["is_admin"] = str(user.is_admin)
    user_dict.pop("hashed_password")
    return user_dict

def normalize(user: UserDB) -> User:
    if user:
        return User(**user.__dict__)
    else:
        return None    

class UserDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all_users(self, limit: int, skip: int) -> list[User]:
        query = await self.db_session.execute(select(UserDB).offset(skip).limit(limit))
        user_array = []
        for user in query.scalars().all():
            user_array.append(normalize(user))
            await UserCache.set(cacheNormalize(normalize(user)))
        return user_array

    async def get_by_id(self, id: int) -> User:
        if (await UserCache.exists(id)):
            return await UserCache.get(id)
        else:
            query = await self.db_session.execute(select(UserDB).where(UserDB.id == id))
            user = normalize(query.scalars().first())
            if user is not None:
                await UserCache.set(cacheNormalize(user))
            else:
                await UserCache.set_null(id)
            return user

    async def create_user(self, user: UserCreate) -> User:
        new_user = UserDB(**user.dict())
        self.db_session.add(new_user)
        await self.db_session.flush()
        new_user_norm = normalize(new_user)
        await UserCache.set(cacheNormalize(new_user_norm))
        return new_user_norm

    async def update_user(self, user: UserUpdate) -> User:
        exists = await self.db_session.execute(select(UserDB.id).where(UserDB.id == user.id))
        exists = exists.scalars().first() is not None
        if exists:
            query = update(UserDB).where(UserDB.id == user.id)
            if user.name:
                query = query.values(name=user.name)
            if user.username:
                query = query.values(username=user.username)
            if user.hashed_password:
                query = query.values(hashed_password=user.hashed_password)
            query = query.values(is_admin=user.is_admin)
            query.execution_options(synchronize_session="fetch")
            await self.db_session.execute(query)
            await UserCache.set(user)
            return user
        else:
            await UserCache.set_null(user.id)
            return None
        
    async def delete_user(self, id: int) -> None:
        query = delete(UserDB).where(UserDB.id == id)
        query.execution_options(synchronize_session="fetch")
        await self.db_session.execute(query)
        await UserCache.delete(id)
        await UserCache.set_null(id)
        