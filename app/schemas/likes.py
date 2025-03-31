from pydantic import BaseModel
from datetime import datetime
from app.config import settings


class LikesBase(BaseModel):
    is_like: bool = True


class LikesCreate(LikesBase):
    pass


class Likes(LikesBase):
    id: int
    user_id: int
    post_id: int
    created: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = cls.from_orm_dict(obj.__dict__)
        data.created = data.created.astimezone(settings.TIMEZONE)
        return cls(**data)
