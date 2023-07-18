from pydantic import BaseModel,validator
from typing import Optional
class Port(BaseModel):
    pod_port: int
    user_port: int

    class Config:
        orm_mode = True


class AppBase(BaseModel):
    name: str
    image: str
    description: str
    switch: str
    ports: list[Port] = []
    volume : str


class AppCreate(AppBase):
    pass


class App(AppBase):
    id: int
    owner_id: int
    host_url: Optional[str] = ""
    class Config:
        orm_mode = True

    @validator('host_url')
    def set_host_url(cls, host_url):
        return host_url or "no url"

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    apps: list[App] = []

    class Config:
        orm_mode = True
