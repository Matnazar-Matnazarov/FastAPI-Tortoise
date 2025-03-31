from app.models.user import User
from app.schemas.user import UserCreate

async def create_user(user: UserCreate):
    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        picture=user.picture,
        phone=user.phone,
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    db_user.set_password(user.password)
    await db_user.save()
    return db_user

async def get_user(user_id: int):
    return await User.get_or_none(id=user_id)

async def get_users():
    return await User.all()