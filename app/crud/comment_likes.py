from app.models.comment_likes import CommentLikes
from app.schemas.comment_likes import CommentLikesCreate


async def create_comment_like(comment_like: CommentLikesCreate, user_id: int, comment_id: int):
    db_comment_like = CommentLikes(**comment_like.dict(), user_id=user_id, comment_id=comment_id)
    await db_comment_like.save()
    return db_comment_like
