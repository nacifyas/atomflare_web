from fastapi import APIRouter, status
from sql.dal.service import ServiceDAL
from models.service import Service, ServiceCreate
from sql.database import async_session

router = APIRouter(
    prefix = "/services"
)

@router.get('/', response_model=list[Service], status_code=status.HTTP_200_OK)
async def get_services(limit: int = 50, skip: int = 0) -> list[Service]:
    async with async_session() as session:
        async with session.begin():
            serviceStream = ServiceDAL(session)
            return await serviceStream.get_all_services(limit, skip)


@router.get('/{service_id}', response_model=Service, status_code=status.HTTP_200_OK)
async def get_service_by_id(service_id: int) -> Service:
    async with async_session() as session:
        async with session.begin():
            service_dal = ServiceDAL(session)
            return await service_dal.get_by_id(service_id)


@router.post('/', response_model=Service, status_code=status.HTTP_201_CREATED)
async def create_service(service: ServiceCreate) -> Service:
    async with async_session() as session:
        async with session.begin():
            new_service = ServiceDAL(session)
            return await new_service.create_service(service)