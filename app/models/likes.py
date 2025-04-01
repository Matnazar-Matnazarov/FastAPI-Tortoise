from tortoise.models import Model
from tortoise import fields
from app.config import settings
from datetime import datetime


class Likes(Model):
    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="likes")
    post = fields.ForeignKeyField("models.Post", related_name="likes")
    is_like = fields.BooleanField(default=True)
    created = fields.DatetimeField(auto_now_add=True, default=lambda: datetime.now(settings.TIMEZONE))
    updated = fields.DatetimeField(auto_now=True, default=lambda: datetime.now(settings.TIMEZONE))

    class Meta:
        table = "likes"
        indexes = [
            ("post_id",),
            ("is_like",),
            ("user_id", "post_id"),
        ]