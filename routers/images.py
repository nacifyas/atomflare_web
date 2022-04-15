from fastapi import APIRouter, status
from sql.dal.image import ImageDAL
from models.image import Image, ImageCreate, ImageUpdate
from sql.database import async_session

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
            return await image_dal.get_by_id(image_id)


@router.post('/', response_model=Image, status_code=status.HTTP_201_CREATED)
async def create_image(image: ImageCreate) -> Image:
    async with async_session() as session:
        async with session.begin():
            new_image = ImageDAL(session)
            return await new_image.create_image(image)


@router.put("/", response_model=ImageUpdate, status_code=status.HTTP_202_ACCEPTED)
async def update_image(image: ImageUpdate) -> None:
    async with async_session() as session:
        async with session.begin():
            image_dal = ImageDAL(session)
            await image_dal.update_image(image)


@router.delete('/{image_id}', status_code=status.HTTP_200_OK)
async def delete_imaged(image_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            image_dal = ImageDAL(session)
            await image_dal.delete_image(image_id)