from typing import Optional
from pydantic import BaseModel

class ServiceBase(BaseModel):
    name: str
    description: str
    logo: str
    link: str
    visibility: Optional[bool] = True

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int

    class Config:
        orm_mode = True


class ServiceUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None
    link: Optional[str] = None
    visibility: Optional[bool] = None

    class Config:
        orm_mode = True