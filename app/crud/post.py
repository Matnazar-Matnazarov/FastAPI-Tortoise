from typing import List, Optional
from app.models.post import Post
from app.schemas.post import PostCreate
from app.crud.images import create_image


async def create_post(post: PostCreate, user_id: int, images: Optional[List] = None) -> Post:
    db_post = Post(**post.model_dump(), user_id=user_id)
    await db_post.save()

    if images:
        for image in images:
            await create_image(image, db_post.id)

    return db_post


async def get_post(post_id: int) -> Optional[Post]:
    return await Post.get_or_none(id=post_id).prefetch_related("images", "comments", "likes")


async def get_posts() -> List[Post]:
    return await Post.all().prefetch_related("images", "comments", "likes")
