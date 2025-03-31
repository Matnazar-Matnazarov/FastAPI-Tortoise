from typing import Optional
from app.models.comment import Comment
from app.schemas.comment import CommentCreate
from app.models.post import Post


async def create_comment(comment: CommentCreate, user_id: int, post_id: int) -> Comment:
    if not await Post.filter(id=post_id).exists():
        raise ValueError("Post not found")

    db_comment = Comment(**comment.model_dump(), user_id=user_id, post_id=post_id)
    await db_comment.save()
    return db_comment


async def get_comment(comment_id: int) -> Optional[Comment]:
    return await Comment.get_or_none(id=comment_id).prefetch_related("comment_likes")
