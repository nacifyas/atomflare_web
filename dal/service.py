from sqlalchemy.orm import Session
from sqlalchemy.future import select
from redis.service import ServiceCache
from sql.sqlmodels import ServiceDB
from models.service import Service, ServiceCreate, ServiceUpdate
from sqlalchemy import delete, update


def normalize(service: ServiceDB) -> Service:
    if service:
        return Service(**service.__dict__)
    else:
        return None

class ServiceDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    async def get_all_services(self, limit: int, skip: int) -> list[Service]:
        query = await self.db_session.execute(select(ServiceDB).offset(skip).limit(limit))
        return [normalize(service) for service in query.scalars().all()]

    async def get_by_id(self, id: int) -> Service:
        if (await ServiceCache.exists(id)):
            return await ServiceCache.get(id)
        else:
            query = await self.db_session.execute(select(ServiceDB).where(ServiceDB.id == id))
            service = normalize(query.scalars().first())
            if service:
                await ServiceCache.set(service)
            else: 
                await ServiceCache.set_null(id)
            return service

    async def create_service(self, service: ServiceCreate) -> Service:
        new_service = ServiceDB(**service.dict())
        self.db_session.add(new_service)
        await self.db_session.flush()
        await ServiceCache.set(new_service)
        return new_service

    async def update_service(self, service: ServiceUpdate) -> Service:
        query = update(ServiceDB).where(ServiceDB.id == service.id)
        if service.name:
            query = query.values(name=service.name)
        if service.description:
            query = query.values(description=service.description)
        if service.logo:
            query = query.values(logo=service.logo)
        if service.link:
            query = query.values(link=service.link)
        query = query.values(is_visible=service.is_visibility)
        query.execution_options(synchronize_session="fetch")
        await self.db_session.execute(query)
        await ServiceCache.set(service)
        return service
        
    async def delete_service(self, id: int) -> None:
        query = delete(ServiceDB).where(ServiceDB.id == id)
        query.execution_options(synchronize_session="fetch")
        await self.db_session.execute(query)
        await ServiceCache.delete(id)
        await ServiceCache.set_null(id)
        
