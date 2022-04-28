from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

metadata = Base.metadata


class ServiceDB(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    logo = Column(String, nullable=False)
    link = Column(String, nullable=False, unique=True)
    is_visible = Column(Boolean, nullable=False, default=True)


class UserDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
