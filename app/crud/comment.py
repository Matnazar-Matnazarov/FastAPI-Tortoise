from app.models.comment import Comment
from app.schemas.comment import CommentCreate


async def create_comment(comment: CommentCreate, user_id: int, post_id: int):
    db_comment = Comment(**comment.dict(), user_id=user_id, post_id=post_id)
    await db_comment.save()
    return db_comment


async def get_comment(comment_id: int):
    return await Comment.get_or_none(id=comment_id).prefetch_related("comment_likes")
