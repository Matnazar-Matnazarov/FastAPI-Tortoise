from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt
from app.config import settings
from datetime import datetime
from fastadmin import TortoiseModelAdmin, register
from uuid import UUID
from passlib.hash import bcrypt


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    is_active = fields.BooleanField(default=True)
    is_staff = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False, null=True)
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


@register(User)
class UserAdmin(TortoiseModelAdmin):
    exclude = ("password",)
    list_display = ("id", "username", "is_superuser", "is_active")
    list_display_links = ("id", "username")
    list_filter = ("id", "username", "is_superuser", "is_active")
    search_fields = ("username",)

    async def authenticate(self, username: str, password: str) -> UUID | int | None:
        user = await User.filter(username=username).first()
        if not user:
            print(f"Foydalanuvchi autopilot: {username}")
            return None
        if not user.check_password(password):
            print(f"Parol noto‘g‘ri: {username}")
            return None
        if not user.is_superuser:
            print(f"Bu foydalanuvchi superuser em's: {username}")
            return None
        print(f"Muvaffaqiyatli kirish: {username}")
        return user.id
