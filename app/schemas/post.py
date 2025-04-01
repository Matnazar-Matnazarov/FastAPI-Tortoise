from pydantic import BaseModel
from datetime import datetime
from app.config import settings
from app.schemas.images import Images
from typing import List
from app.models.images import Images as ImagesModel

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
        data = obj.__dict__
        data["created"] = data["created"].astimezone(settings.TIMEZONE)
        if "updated" in data:
            data["updated"] = data["updated"].astimezone(settings.TIMEZONE)
        return cls(**data)


class PostImage(PostBase):
    id: int
    user_id: int
    created: datetime
    updated: datetime
    images: List[Images]

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = obj.__dict__
        data["created"] = data["created"].astimezone(settings.TIMEZONE)
        data["updated"] = data["updated"].astimezone(settings.TIMEZONE)
        data["images"] = [Images.from_orm(img) for img in obj.images]
        return cls(**data)