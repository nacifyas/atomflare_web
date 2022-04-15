from pydantic import BaseModel
from typing import Optional

class ImageBase(BaseModel):
    title: str
    description: str
    url: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True

class ImageUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True