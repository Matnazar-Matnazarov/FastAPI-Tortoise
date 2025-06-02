from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas.user import User, UserCreate
from app.crud.user import create_user, get_user, get_users
from app.auth.jwt import get_current_user
from app.models.user import User as UserModel
from fastapi.responses import FileResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate):
    try:
        return await create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int, current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    db_user = await get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.get("/", response_model=List[User])
async def read_users(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return await get_users()
