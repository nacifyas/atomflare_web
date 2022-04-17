from typing import Optional
from fastapi import Query
from pydantic import BaseModel

class UserBase(BaseModel):
    username: Optional[str] = Query(..., min_length=3, max_length=10)
    name: Optional[str] = Query(..., min_length=3, max_length=10)

class UserCreate(UserBase):
    hashed_password: Optional[str]
    is_admin: Optional[bool] = False

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    id: int
    username: Optional[str] = Query(None, min_length=3, max_length=10)
    name: Optional[str] = Query(None, min_length=3, max_length=10)
    hashed_password: Optional[str] = None
    is_admin: Optional[bool] = None