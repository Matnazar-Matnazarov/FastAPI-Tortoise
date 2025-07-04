from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.images import Images
from app.crud.images import get_image, get_images_by_post, delete_image
from app.auth.jwt import get_current_user
from app.models.user import User
from app.models.post import Post

router = APIRouter(prefix="/images", tags=["images"])


@router.get("/{image_id}", response_model=Images)
async def read_image(image_id: int, current_user: User = Depends(get_current_user)):
    db_image = await get_image(image_id)
    if db_image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )

    post = await Post.get_or_none(id=db_image.post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post.user_id != current_user.id and not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view this image",
        )
    return db_image


@router.get("/post/{post_id}", response_model=List[Images])
async def read_images_by_post(
    post_id: int, current_user: User = Depends(get_current_user)
):
    post = await Post.get_or_none(id=post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post.user_id != current_user.id and not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view images of this post",
        )

    try:
        return await get_images_by_post(post_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image_endpoint(
    image_id: int, current_user: User = Depends(get_current_user)
):
    db_image = await get_image(image_id)
    if db_image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )

    post = await Post.get_or_none(id=db_image.post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post.user_id != current_user.id and not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this image",
        )

    try:
        await delete_image(image_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
