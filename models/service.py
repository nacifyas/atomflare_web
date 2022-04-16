from typing import Optional
from fastapi import Query
from pydantic import BaseModel

class ServiceBase(BaseModel):
    name: Optional[str] = Query(..., min_length=3, max_length=75)
    description: Optional[str] = Query(..., min_length=3, max_length=140)
    logo: str = Query(..., regex="^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
    link: str = Query(..., regex="^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
    visibility: Optional[bool] = True

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
    logo: str = Query(None, regex="^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
    link: str = Query(None, regex="^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
    visibility: Optional[bool] = None

    class Config:
        orm_mode = True