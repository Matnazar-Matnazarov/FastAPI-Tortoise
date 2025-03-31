from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.responses import FileResponse
from app.schemas.post import Post, PostCreate
from app.schemas.images import ImagesCreate
from app.crud.post import create_post, get_post, get_posts
from app.crud.images import create_image
from app.auth.jwt import get_current_user
from app.models.user import User
from pathlib import Path

router = APIRouter(prefix="/posts", tags=["posts"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_new_post(
        post: PostCreate,
        images: Optional[List[UploadFile]] = File(None),
        current_user: User = Depends(get_current_user),
):
    image_list = []
    if images:
        for image in images:
            file_path = UPLOAD_DIR / f"{image.filename}"
            with file_path.open("wb") as buffer:
                buffer.write(await image.read())
            image_list.append(ImagesCreate(image=str(file_path), is_active=True))

    try:
        return await create_post(post, current_user.id, images=image_list)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{post_id}", response_model=Post)
async def read_post(post_id: int, current_user: User = Depends(get_current_user)):
    db_post = await get_post(post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if db_post.user_id != current_user.id and not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view this post",
        )
    return db_post


@router.get("/", response_model=List[Post])
async def read_posts(current_user: User = Depends(get_current_user)):
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view all posts",
        )
    return await get_posts()


@router.get("/images/{image_path:path}", response_class=FileResponse)
async def get_image(image_path: str):
    file_path = Path(image_path)
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return FileResponse(file_path)
