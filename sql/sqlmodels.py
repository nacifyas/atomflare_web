from sqlalchemy import Column, Integer, String, Boolean

from .database import Base


class ImageDB(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    url = Column(String, nullable=False)

class ServiceDB(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    logo = Column(String, nullable=False)
    link = Column(String, nullable=False)
    visibility = Column(Boolean, nullable=False)