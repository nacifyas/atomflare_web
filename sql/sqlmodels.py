from sqlalchemy import Column, Integer, String

from .database import Base

class ImageDB(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)