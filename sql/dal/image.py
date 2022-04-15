from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sql.sqlmodels import ImageDB
from models.image import Image, ImageCreate, ImageUpdate
from sqlalchemy import update, delete

def normalize(image: ImageDB) -> Image:
    return Image(id=image.id, description=image.description, title=image.title, url=image.url)

class ImageDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all_images(self, limit: int, skip: int) -> list[Image]:
        query = await self.db_session.execute(select(ImageDB).offset(skip).limit(limit))
        return [normalize(image) for image in query.scalars().all()]

    async def get_by_id(self, id: int):
        query = await self.db_session.execute(select(ImageDB).where(ImageDB.id == id))
        return normalize(query.scalars().first())

    async def create_image(self, image: ImageCreate) -> Image:
        new_image = ImageDB(**image.dict())
        self.db_session.add(new_image)
        await self.db_session.flush()
        return new_image

    async def update_image(self, image: ImageUpdate) -> None:
        query = update(ImageDB).where(ImageDB.id == image.id)
        if image.title:
            query = query.values(title=image.title)
        if image.description:
            query = query.values(description=image.description)
        query.execution_options(synchronize_session="fetch")
        await self.db_session.execute(query)

    async def delete_image(self, id: int) -> None:
        query = delete(ImageDB).where(ImageDB.id == id)
        query.execution_options(synchronize_session="fetch")
        await self.db_session.execute(query)
