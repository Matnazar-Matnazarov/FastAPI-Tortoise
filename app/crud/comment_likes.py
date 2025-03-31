from typing import Optional
from app.models.comment_likes import CommentLikes
from app.schemas.comment_likes import CommentLikesCreate
from app.models.comment import Comment


async def create_comment_like(comment_like: CommentLikesCreate, user_id: int, comment_id: int) -> CommentLikes:
    if not await Comment.filter(id=comment_id).exists():
        raise ValueError("Comment not found")

    if await CommentLikes.filter(user_id=user_id, comment_id=comment_id).exists():
        raise ValueError("User has already liked this comment")

    db_comment_like = CommentLikes(**comment_like.model_dump(), user_id=user_id, comment_id=comment_id)
    await db_comment_like.save()
    return db_comment_like


async def get_comment_like(comment_like_id: int) -> Optional[CommentLikes]:
    return await CommentLikes.get_or_none(id=comment_like_id)
