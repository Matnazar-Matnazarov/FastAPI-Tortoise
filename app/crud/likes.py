from typing import Optional
from app.models.likes import Likes
from app.schemas.likes import LikesCreate
from app.models.post import Post


async def create_like(like: LikesCreate, user_id: int, post_id: int) -> Likes:
    if not await Post.filter(id=post_id).exists():
        raise ValueError("Post not found")

    if await Likes.filter(user_id=user_id, post_id=post_id).exists():
        raise ValueError("User has already liked this post")

    db_like = Likes(**like.model_dump(), user_id=user_id, post_id=post_id)
    await db_like.save()
    return db_like


async def get_like(like_id: int) -> Optional[Likes]:
    return await Likes.get_or_none(id=like_id)
