from pydantic import BaseModel
from datetime import datetime
from app.config import settings


class CommentBase(BaseModel):
    comment: str
    is_active: bool = True


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
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
