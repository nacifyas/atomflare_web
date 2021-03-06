from typing import Optional
from fastapi import Query
from pydantic import BaseModel

ATRIBUTES_LIST = ["id", "username", "name", "is_admin", "hashed_password"]


class UserBase(BaseModel):
    username: Optional[str] = Query(..., min_length=3, max_length=25)
    name: Optional[str] = Query(..., min_length=3, max_length=75)
    is_admin: Optional[bool] = False


class UserCreate(UserBase):
    hashed_password: str


class User(UserCreate):
    id: int

    class Config:
        orm_mode = True


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    id: int
    username: Optional[str] = Query(None, min_length=3, max_length=10)
    name: Optional[str] = Query(None, min_length=3, max_length=10)
    hashed_password: Optional[str]
    is_admin: Optional[bool] = False
