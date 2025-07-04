from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.comment_likes import CommentLikes, CommentLikesCreate
from app.crud.comment_likes import create_comment_like, get_comment_like
from app.auth.jwt import get_current_user
from app.models.user import User
from app.models.comment import Comment

router = APIRouter(prefix="/comment-likes", tags=["comment_likes"])


@router.post(
    "/{comment_id}", response_model=CommentLikes, status_code=status.HTTP_201_CREATED
)
async def create_new_comment_like(
    comment_id: int,
    comment_like: CommentLikesCreate,
    current_user: User = Depends(get_current_user),
):
    if not await Comment.filter(id=comment_id).exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    try:
        return await create_comment_like(comment_like, current_user.id, comment_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{comment_like_id}", response_model=CommentLikes)
async def read_comment_like(
    comment_like_id: int, current_user: User = Depends(get_current_user)
):
    db_comment_like = await get_comment_like(comment_like_id)
    if db_comment_like is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment like not found"
        )
    if db_comment_like.user_id != current_user.id and not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view this comment like",
        )
    return db_comment_like
