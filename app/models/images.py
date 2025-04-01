from tortoise.models import Model
from tortoise import fields
from app.config import settings
from datetime import datetime


class Images(Model):
    id = fields.BigIntField(pk=True)
    image = fields.CharField(max_length=255)
    post = fields.ForeignKeyField("models.Post", related_name="images")
    is_active = fields.BooleanField(default=True)
    created = fields.DatetimeField(auto_now_add=True, default=lambda: datetime.now(settings.TIMEZONE))
    updated = fields.DatetimeField(auto_now=True, default=lambda: datetime.now(settings.TIMEZONE))

    class Meta:
        table = "images"
        indexes = [
            ("post_id",),
            ("is_active",),
            ("post_id", "is_active"),
        ]

