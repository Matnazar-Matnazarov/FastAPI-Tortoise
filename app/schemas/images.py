from pydantic import BaseModel
from datetime import datetime
from app.config import settings

class ImagesBase(BaseModel):
    image: str
    is_active: bool = True

class ImagesCreate(ImagesBase):
    pass

class Images(ImagesBase):
    id: int
    post: int
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
        data["post"] = data["post_id"]
        return cls(**data)
