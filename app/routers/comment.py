from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.comment import Comment, CommentCreate
from app.crud.comment import create_comment, get_comment
from app.auth.jwt import get_current_user
from app.models.user import User
from app.models.post import Post

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/{post_id}", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_new_comment(
    post_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
):
    """Postga yangi izoh qo'shadi.

    Args:
        post_id (int): Post ID'si.
        comment (CommentCreate): Izoh ma'lumotlari.
        current_user (User): Joriy autentifikatsiya qilingan foydalanuvchi.

    Returns:
        Comment: Yaratilgan izoh obyekti.

    Raises:
        HTTPException: Agar post topilmasa.
    """
    if not await Post.filter(id=post_id).exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    try:
        return await create_comment(comment, current_user.id, post_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{comment_id}", response_model=Comment)
async def read_comment(comment_id: int, current_user: User = Depends(get_current_user)):
    db_comment = await get_comment(comment_id)
    if db_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if db_comment.user_id != current_user.id and not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view this comment",
        )
    return db_comment