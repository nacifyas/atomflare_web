from typing import Optional
from fastapi import Query
from pydantic import BaseModel

ATRIBUTES_LIST = ["id", "name", "description", "logo", "link", "is_visible"]


class ServiceBase(BaseModel):
    name: Optional[str] = Query(..., min_length=3, max_length=75)
    description: Optional[str] = Query(..., min_length=3, max_length=140)
    logo: Optional[str] = Query(..., min_length=3, max_length=70)
    link: Optional[str] = Query(..., min_length=3, max_length=170)
    is_visible: Optional[bool] = True


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    id: int

    class Config:
        orm_mode = True


class ServiceUpdate(BaseModel):
    id: int
    name: Optional[str] = Query(None, min_length=3, max_length=75)
    description: Optional[str] = Query(None, min_length=3, max_length=140)
    logo: Optional[str] = Query(None, min_length=4, max_length=70)
    link: Optional[str] = Query(None, min_length=4, max_length=170)
    is_visible: Optional[bool] = None

    class Config:
        orm_mode = True
