from pydantic import BaseModel
from datetime import datetime
from app.config import settings
from app.schemas.user import User


class LikesBase(BaseModel):
    is_like: bool = True


class LikesCreate(LikesBase):
    pass


class Likes(LikesBase):
    id: int
    user_id: int
    post_id: int
    created: datetime
    user: "User"

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = obj.__dict__
        data["created"] = data["created"].astimezone(settings.TIMEZONE)
        if "updated" in data:
            data["updated"] = data["updated"].astimezone(settings.TIMEZONE)
        if hasattr(obj, "user"):
            data["user"] = User.from_orm(obj.user)
        return cls(**data)
