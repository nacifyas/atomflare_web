from pydantic import BaseModel

class ServiceBase(BaseModel):
    name: str
    description: str
    logo: str
    link: str

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int

    class Config:
        orm_mode = True