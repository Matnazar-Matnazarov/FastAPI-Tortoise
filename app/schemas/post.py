from pydantic import BaseModel
from datetime import datetime
from app.config import settings


class PostBase(BaseModel):
    name: str
    title: str
    text: str
    is_active: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    user_id: int
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = cls.from_orm_dict(obj.__dict__)
        data.created = data.created.astimezone(settings.TIMEZONE)
        data.updated = data.updated.astimezone(settings.TIMEZONE)
        return cls(**data)
