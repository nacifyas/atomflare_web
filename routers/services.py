from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError
from dal.service import ServiceDAL
from sql.database import async_session
from models.service import Service, ServiceCreate, ServiceUpdate
from auth.dependencies import oauth2_scheme, current_user_admin

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
            ret = await service_dal.get_by_id(service_id)
            if ret:
                return ret
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such service")
                

@router.post('/', response_model=Service, dependencies=[Depends(oauth2_scheme), Depends(current_user_admin)], status_code=status.HTTP_201_CREATED)
async def create_service(service: ServiceCreate) -> Service:
    async with async_session() as session:
        async with session.begin():
            new_service = ServiceDAL(session)
            try:
                return await new_service.create_service(service)
            except IntegrityError as e:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=e.orig.args[0])


@router.put("/", dependencies=[Depends(oauth2_scheme), Depends(current_user_admin)], status_code=status.HTTP_204_NO_CONTENT)
async def update_service(service: ServiceUpdate):
    async with async_session() as session:
        async with session.begin():
            service_dal = ServiceDAL(session)
            try:     
                updated_service = await service_dal.update_service(service)
                if updated_service is None:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such service")
            except IntegrityError as e:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=e.orig.args[0])
            else:
                return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{service_id}", dependencies=[Depends(oauth2_scheme), Depends(current_user_admin)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_id: int):
    async with async_session() as session:
        async with session.begin():
            service_dal = ServiceDAL(session)
            await service_dal.delete_service(service_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)