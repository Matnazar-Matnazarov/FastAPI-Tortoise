from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.likes import Likes, LikesCreate
from app.crud.likes import create_like, get_like
from app.auth.jwt import get_current_user
from app.models.user import User
from app.models.post import Post

router = APIRouter(prefix="/likes", tags=["likes"])


@router.post("/{post_id}", response_model=Likes, status_code=status.HTTP_201_CREATED)
async def create_new_like(
    post_id: int,
    like: LikesCreate,
    current_user: User = Depends(get_current_user),
):
    if not await Post.filter(id=post_id).exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    try:
        return await create_like(like, current_user.id, post_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{like_id}", response_model=Likes)
async def read_like(like_id: int, current_user: User = Depends(get_current_user)):
    db_like = await get_like(like_id)
    if db_like is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Like not found"
        )
    if db_like.user_id != current_user.id and not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view this like",
        )
    return db_like
