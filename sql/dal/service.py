from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sql.sqlmodels import ServiceDB
from models.service import Service, ServiceCreate

def normalize(service: ServiceDB) -> Service:
    return Service(id=service.id, name=service.name, description=service.description, logo=service.logo, link=service.link, visibility=service.visibility)

class ServiceDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    async def get_all_services(self, limit: int, skip: int) -> list[Service]:
        query = await self.db_session.execute(select(ServiceDB).offset(skip).limit(limit))
        return [normalize(service) for service in query.scalars().all()]

    async def get_by_id(self, id: int) -> Service:
        query = await self.db_session.execute(select(ServiceDB).where(ServiceDB.id == id))
        return normalize(query.scalars().first())

    async def create_service(self, service: ServiceCreate) -> Service:
        new_service = ServiceDB(**service.dict())
        self.db_session.add(new_service)
        await self.db_session.flush()
        return new_service