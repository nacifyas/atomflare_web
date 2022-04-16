from pydantic import BaseModel
from typing import Optional
from fastapi import Query

class ImageBase(BaseModel):
    title: Optional[str] = Query(..., min_length=3, max_length=75)
    description: Optional[str] = Query(..., min_length=5, max_length=160)
    url: str = Query(..., regex="^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True

class ImageUpdate(BaseModel):
    id: int
    title: Optional[str] = Query(None, min_length=3, max_length=75)
    description: Optional[str] = Query(None, min_length=5, max_length=160)

    class Config:
        orm_mode = True