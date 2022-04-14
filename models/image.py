from pydantic import BaseModel
import sql.models as QuerriedImage

class ImageBase(BaseModel):
    title: str
    description: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True