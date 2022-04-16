from fastapi import APIRouter, status, HTTPException
from fastapi.responses import Response
from sql.dal.image import ImageDAL
from sql.database import async_session
from models.image import Image, ImageCreate, ImageUpdate

router = APIRouter(
    prefix = "/gallery"
)

@router.get('/', response_model=list[Image], status_code=status.HTTP_200_OK)
async def get_gallery(limit: int = 50, skip: int = 0) -> list[Image]:
    async with async_session() as session:
        async with session.begin():
            imageStream = ImageDAL(session)
            return await imageStream.get_all_images(limit, skip)


@router.get('/{image_id}', response_model=Image, status_code=status.HTTP_200_OK)
async def get_image_by_id(image_id: int) -> Image:
    async with async_session() as session:
        async with session.begin():
            image_dal = ImageDAL(session)
            ret = await image_dal.get_by_id(image_id)
            if ret:
                return ret
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
                

@router.post('/', response_model=Image, status_code=status.HTTP_201_CREATED)
async def create_image(image: ImageCreate) -> Image:
    async with async_session() as session:
        async with session.begin():
            new_image = ImageDAL(session)
            try:
                return await new_image.create_image(image)
            except Exception:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The input data is not valid")



@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_image(image: ImageUpdate) -> None:
    async with async_session() as session:
        async with session.begin():
            image_dal = ImageDAL(session)
            try:
                await image_dal.update_image(image)
            except Exception:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The input data is not valid")
            else:
                return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/{image_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_imaged(image_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            image_dal = ImageDAL(session)
            await image_dal.delete_image(image_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)