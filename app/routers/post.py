from fastapi import APIRouter, HTTPException, Depends
from app.schemas.post import Post, PostCreate
from app.crud.post import create_post, get_post, get_posts
from app.auth.jwt import get_current_user
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=Post)
async def create_new_post(post: PostCreate, current_user: User = Depends(get_current_user)):
    db_post = await create_post(post, current_user.id)
    return db_post


@router.get("/{post_id}", response_model=Post)
async def read_post(post_id: int, current_user: User = Depends(get_current_user)):
    db_post = await get_post(post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.get("/", response_model=list[Post])
async def read_posts(current_user: User = Depends(get_current_user)):
    return await get_posts()
