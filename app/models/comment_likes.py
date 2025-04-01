from tortoise.models import Model
from tortoise import fields
from app.config import settings
from datetime import datetime


class CommentLikes(Model):
    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="comment_likes")
    comment = fields.ForeignKeyField("models.Comment", related_name="comment_likes")
    is_like = fields.BooleanField(default=True)
    created = fields.DatetimeField(auto_now_add=True, default=lambda: datetime.now(settings.TIMEZONE))
    updated = fields.DatetimeField(auto_now=True, default=lambda: datetime.now(settings.TIMEZONE))

    class Meta:
        table = "comment_likes"
        indexes = [
            ("comment_id",),
            ("is_like",),
            ("user_id", "comment_id", "is_like"),
            ("user_id", "comment_id", "created"),
        ]

