from fastapi import APIRouter
from sql.dal.image import ImageDAL
from models.image import ImageBase, ImageCreate
from sql.database import async_session

router = APIRouter(
    prefix = "/gallery"
)

# @router.get('/', response_model=list[ImageBase])
@router.get('/')
async def get_gallery(): # -> list[ImageBase]:
    async with async_session() as session:
        async with session.begin():
            imageStream = ImageDAL(session)
            return await imageStream.get_all_images()


# @router.get('/{image_id}', response_model=ImageBase)
@router.get('/{image_id}')
async def get_image_by_id(image_id: int):
    async with async_session() as session:
        async with session.begin():
            image_dal = ImageDAL(session)
            return await image_dal.get_by_id(image_id)


# @router.post('/', response_model=ImageCreate)
@router.post('/')
async def create_image(image: ImageCreate):
    async with async_session() as session:
        async with session.begin():
            new_image = ImageDAL(session)
            return await new_image.create_image(image)