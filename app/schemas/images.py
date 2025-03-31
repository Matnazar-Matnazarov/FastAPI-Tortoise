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
    post_id: int
    created: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = cls.from_orm_dict(obj.__dict__)
        data.created = data.created.astimezone(settings.TIMEZONE)
        return cls(**data)
