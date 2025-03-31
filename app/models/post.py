from tortoise.models import Model
from tortoise import fields
from app.config import settings
from datetime import datetime


class Post(Model):
    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="posts")
    name = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)
    text = fields.TextField()
    is_active = fields.BooleanField(default=True)
    created = fields.DatetimeField(auto_now_add=True, default=lambda: datetime.now(settings.TIMEZONE))
    updated = fields.DatetimeField(auto_now=True, default=lambda: datetime.now(settings.TIMEZONE))

    images = fields.ReverseRelation["Images"]
    comments = fields.ReverseRelation["Comment"]
    likes = fields.ReverseRelation["Likes"]

    class Meta:
        table = "post"
