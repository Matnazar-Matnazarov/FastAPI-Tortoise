from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt
from app.config import settings
from datetime import datetime


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    is_active = fields.BooleanField(default=True)
    is_staff = fields.BooleanField(default=False)
    picture = fields.CharField(max_length=255, null=True)
    phone = fields.CharField(max_length=20, null=True)
    created = fields.DatetimeField(auto_now_add=True, default=lambda: datetime.now(settings.TIMEZONE))
    updated = fields.DatetimeField(auto_now=True, default=lambda: datetime.now(settings.TIMEZONE))

    posts = fields.ReverseRelation["Post"]
    comments = fields.ReverseRelation["Comment"]
    likes = fields.ReverseRelation["Likes"]
    comment_likes = fields.ReverseRelation["CommentLikes"]

    class Meta:
        table = "users"
        indexes = [
            ("is_staff",),
            ("username", "email"),
        ]

    def set_password(self, raw_password: str):
        self.password = bcrypt.hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.verify(raw_password, self.password)
