from sqlalchemy.orm import Session
from sqlalchemy.future import select
from models.image import Image, ImageCreate
from ..sqlmodels import ImageDB

def normalize(image: ImageDB) -> Image:
    return image[ImageDB]

class ImageDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all_images(self, limit: int, skip: int) -> list[Image]:
        query = await self.db_session.execute(select(ImageDB).offset(skip).limit(limit))
        return [normalize(image) for image in query.all()]

    async def get_by_id(self, id: int):
        query = await self.db_session.execute(select(ImageDB).where(ImageDB.id == id))
        return normalize(query.first())

    async def create_image(self, image: ImageCreate):
        new_image = ImageDB(**image.dict())
        self.db_session.add(new_image)
        await self.db_session.flush()
        return new_image