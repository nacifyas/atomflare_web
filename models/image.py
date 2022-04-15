from pydantic import BaseModel

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