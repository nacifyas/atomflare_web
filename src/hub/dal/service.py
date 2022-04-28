from typing import Optional, Union
from sqlalchemy.orm import Session
from hub.sql.database import async_session
from sqlalchemy.future import select
from hub.redis.service import ServiceCache
from hub.sql.sqlmodels import ServiceDB
from hub.models.service import Service, ServiceCreate, ServiceUpdate
from sqlalchemy import delete, update
import asyncio


def cacheNormalize(service: Union[Service, ServiceDB]) -> dict:
    service_dict = service.dict() if isinstance(service, Service) else Service(**service.__dict__).dict()
    service_dict["is_visible"] = str(service.is_visible)
    return service_dict


def normalize(service: ServiceDB) -> Service:
    if service is not None:
        return Service(**service.__dict__)
    else:
        return None


class ServiceDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all_services(self, limit: int, skip: int) -> list[Service]:
        query = await self.db_session.execute(select(ServiceDB).offset(skip).limit(limit))
        coro_arr = []
        service_array = []
        for service in query.scalars().all():
            service_array.append(normalize(service))
            coro_arr.append(
                ServiceCache().set(cacheNormalize(service))
            )
        await asyncio.gather(*coro_arr)
        return service_array

    async def get_by_id(self, id: int) -> Optional[Service]:
        service_exists, service_retrieval = await asyncio.gather(
            ServiceCache().exists(id),
            ServiceCache().get(id)
        )
        if (service_exists):
            return service_retrieval
        else:
            query = await self.db_session.execute(select(ServiceDB).where(ServiceDB.id == id))
            service = normalize(query.scalars().first())
            if service is not None:
                await ServiceCache().set(cacheNormalize(service))
            else:
                await ServiceCache().set_null(id)
            return service

    async def create_service(self, service: ServiceCreate) -> Service:
        new_service = ServiceDB(**service.dict())
        self.db_session.add(new_service)
        await self.db_session.flush()
        await ServiceCache().set(cacheNormalize(new_service))
        return normalize(new_service)

    async def update_service(self, service: ServiceUpdate) -> Optional[Service]:
        old_service = await self.get_by_id(service.id)
        service_cache = ServiceCache()
        if old_service is not None:
            query = update(ServiceDB).where(ServiceDB.id == service.id)
            if service.name:
                query = query.values(name=service.name)
                old_service.name = service.name
            if service.description:
                query = query.values(description=service.description)
                old_service.description = service.description
            if service.logo:
                query = query.values(logo=service.logo)
                old_service.logo = service.logo
            if service.link:
                query = query.values(link=service.link)
                old_service.link = service.link
            if service.is_visible is not None:
                query = query.values(is_visible=service.is_visible)
                old_service.is_visible = service.is_visible
            query.execution_options(synchronize_session="fetch")
            await self.db_session.execute(query)
            await service_cache.set(cacheNormalize(old_service))
            return old_service
        else:
            await service_cache.set_null(service.id)
            return None

    async def delete_service(self, id: int) -> None:
        query = delete(ServiceDB).where(ServiceDB.id == id)
        query.execution_options(synchronize_session="fetch")
        await asyncio.gather(
            self.db_session.execute(query),
            ServiceCache().delete(id),
            ServiceCache().set_null(id)
        )


async def begin() -> ServiceDAL:
    async with async_session() as session:
        async with session.begin():
            return ServiceDAL(session)
