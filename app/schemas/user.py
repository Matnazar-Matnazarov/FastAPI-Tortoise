from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.config import settings


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    is_active: bool = True
    is_staff: bool = False
    picture: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = cls.from_orm_dict(obj.__dict__)
        data.created = data.created.astimezone(settings.TIMEZONE)
        return cls(**data)


class LoginForm(BaseModel):
    username: str
    password: str
