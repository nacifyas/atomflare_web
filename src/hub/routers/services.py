from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError
from hub.dal.dependencies import get_service_dal
from hub.dal.service import ServiceDAL
from hub.models.service import Service, ServiceCreate, ServiceUpdate
from hub.auth.dependencies import oauth2_scheme, current_user_admin

router = APIRouter(
    prefix="/services"
)


@router.get('/', response_model=list[Service], status_code=status.HTTP_200_OK)
async def get_services(limit: int = 50, skip: int = 0, service_dal: ServiceDAL = Depends(get_service_dal)) -> list[Service]:
    return await service_dal.get_all_services(limit, skip)


@router.get('/{service_id}', response_model=Service, status_code=status.HTTP_200_OK)
async def get_service_by_id(service_id: int, service_dal: ServiceDAL = Depends(get_service_dal)) -> Service:
    ret = await service_dal.get_by_id(service_id)
    if ret is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such service"
            )
    else:
        return ret


@router.post('/', response_model=Service, dependencies=[Depends(oauth2_scheme), Depends(current_user_admin)], status_code=status.HTTP_201_CREATED)
async def create_service(service: ServiceCreate, service_dal: ServiceDAL = Depends(get_service_dal)) -> Service:
    try:
        return await service_dal.create_service(service)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=e.orig.args[0]
            )


@router.put("/", dependencies=[Depends(oauth2_scheme), Depends(current_user_admin)], status_code=status.HTTP_204_NO_CONTENT)
async def update_service(service: ServiceUpdate, service_dal: ServiceDAL = Depends(get_service_dal)) -> Response:
    try:
        updated_service = await service_dal.update_service(service)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=e.orig.args[0]
            )
    else:
        if updated_service is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such service"
                )
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{service_id}", dependencies=[Depends(oauth2_scheme), Depends(current_user_admin)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_id: int, service_dal: ServiceDAL = Depends(get_service_dal)) -> Response:
    await service_dal.delete_service(service_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
