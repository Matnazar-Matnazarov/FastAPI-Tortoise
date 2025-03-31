from tortoise.models import Model
from tortoise import fields
from datetime import datetime
from app.config import settings


class Comment(Model):
    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="comments")
    post = fields.ForeignKeyField("models.Post", related_name="comments")
    comment = fields.TextField()
    is_active = fields.BooleanField(default=True)
    created = fields.DatetimeField(auto_now_add=True, default=lambda: datetime.now(settings.TIMEZONE))
    updated = fields.DatetimeField(auto_now=True, default=lambda: datetime.now(settings.TIMEZONE))

    comment_likes = fields.ReverseRelation["CommentLikes"]

    class Meta:
        table = "comment"
