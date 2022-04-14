from sqlalchemy.orm import Session
from sqlalchemy.future import select
from models.image import ImageBase, ImageCreate
from ..models import ImageDB

class ImageDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session


    async def get_all_images(self):# -> list[ImageBase]:
        query = await self.db_session.execute(select(ImageDB))
        return query.all()


    async def get_by_id(self, id: int):
        query = await self.db_session.execute(select(ImageDB).where(ImageDB.id == id))
        return query.first()

    async def create_image(self, image: ImageCreate):
        new_image = ImageDB(**image.dict())
        self.db_session.add(new_image)
        await self.db_session.flush()
        return new_image