from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.user import UserCreate, LoginForm
from app.crud.user import create_user
from app.auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=dict)
async def register(user: UserCreate):
    db_user = await User.filter(username=user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = await User.filter(email=user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_user(user)
    access_token = create_access_token({"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login-form", response_model=dict)
async def login_form(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if not user or not user.check_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login-json", response_model=dict)
async def login_json(form_data: LoginForm):
    user = await User.get_or_none(username=form_data.username)
    if not user or not user.check_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
