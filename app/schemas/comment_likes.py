from pydantic import BaseModel
from datetime import datetime
from app.config import settings


class CommentLikesBase(BaseModel):
    is_like: bool = True


class CommentLikesCreate(CommentLikesBase):
    pass


class CommentLikes(CommentLikesBase):
    id: int
    user_id: int
    comment_id: int
    created: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = cls.from_orm_dict(obj.__dict__)
        data.created = data.created.astimezone(settings.TIMEZONE)
        return cls(**data)
