from app.models.likes import Likes
from app.schemas.likes import LikesCreate


async def create_like(like: LikesCreate, user_id: int, post_id: int):
    db_like = Likes(**like.dict(), user_id=user_id, post_id=post_id)
    await db_like.save()
    return db_like
