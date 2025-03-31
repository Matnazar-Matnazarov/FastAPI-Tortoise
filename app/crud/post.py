from app.models.post import Post
from app.schemas.post import PostCreate

async def create_post(post: PostCreate, user_id: int):
    db_post = Post(**post.dict(), user_id=user_id)
    await db_post.save()
    return db_post

async def get_post(post_id: int):
    return await Post.get_or_none(id=post_id).prefetch_related("images", "comments", "likes")

async def get_posts():
    return await Post.all().prefetch_related("images", "comments", "likes")