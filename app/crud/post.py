from typing import List, Optional
from app.models.post import Post
from app.schemas.post import PostCreate
from app.crud.images import create_image
from app.schemas.post import PostImage

async def create_post(post: PostCreate, user_id: int, images: Optional[List] = None) -> Post:
    db_post = Post(**post.model_dump(), user_id=user_id)
    await db_post.save()

    if images:
        for image in images:
            await create_image(image, db_post.id)

    return await Post.get(id=db_post.id).prefetch_related("images", "comments", "likes")


async def get_post(post_id: int) -> Optional[PostImage]:
    post = await Post.get_or_none(id=post_id).prefetch_related(
        "images",
        "comments",
        "likes",
        "comments__user",
        "likes__user"
    )
    if post:
        return PostImage.from_orm(post)
    return None


async def get_posts() -> List[PostImage]:
    posts = await Post.filter(is_active=True).prefetch_related(
        "images",
        "comments",
        "likes",
        "comments__user",
        "likes__user"
    )
    return [PostImage.from_orm(post) for post in posts]


async def update_post(post_id: int, post_data: PostCreate, images: Optional[List] = None) -> Optional[Post]:
    db_post = await Post.get_or_none(id=post_id)
    if not db_post:
        return None

    for key, value in post_data.model_dump(exclude_unset=True).items():
        setattr(db_post, key, value)
    await db_post.save()

    # Update images if provided
    if images is not None:
        await db_post.images.all().delete()
        for image in images:
            await create_image(image, db_post.id)

    return await Post.get(id=post_id).prefetch_related("images", "comments", "likes")


async def delete_post(post_id: int) -> bool:
    db_post = await Post.get_or_none(id=post_id)
    if not db_post:
        return False
    await db_post.delete()
    return True
