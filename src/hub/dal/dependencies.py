from hub.dal.service import ServiceDAL
from hub.dal.user import UserDAL
from hub.sql.database import async_session


async def get_service_dal() -> ServiceDAL:
    async with async_session() as session:
        async with session.begin():
            return ServiceDAL(session)


async def get_user_dal() -> UserDAL:
    async with async_session() as session:
        async with session.begin():
            return UserDAL(session)
