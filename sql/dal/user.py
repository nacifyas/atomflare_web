from sqlalchemy.orm import Session
from sql.sqlmodels import UserDB
from models.user import User, UserCreate, UserUpdate
from sqlalchemy.future import select
from sqlalchemy import delete, update

def normalize(user: UserDB) -> User:
    if user:
        return User(**user.__dict__)
    else:
        return None    

class UserDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_by_username(self, username: str) -> User:
        query = await self.db_session.execute(select(UserDB).where(UserDB.username == username))
        return normalize(query.scalars().first())


    async def get_all_users(self, limit: int, skip: int) -> list[User]:
        query = await self.db_session.execute(select(UserDB).offset(skip).limit(limit))
        return [normalize(user) for user in query.scalars().all()]


    async def create_user(self, user: UserCreate) -> User:
        new_user = UserDB(**user.dict())
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def update_user(self, user: UserUpdate) -> None:
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
        return user
        
    async def delete_user(self, id: int) -> None:
        query = delete(UserDB).where(UserDB.id == id)
        query.execution_options(synchronize_session="fetch")
        await self.db_session.execute(query)
        