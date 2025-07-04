from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from app.config import settings
from app.models.user import User

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", settings.JWT_SECRET_KEY)
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", settings.JWT_ALGORITHM)
JWT_EXPIRY_MINUTES = int(os.getenv("JWT_EXPIRY_MINUTES", settings.JWT_EXPIRY_MINUTES))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(settings.TIMEZONE) + expires_delta
    else:
        expire = datetime.now(settings.TIMEZONE) + timedelta(minutes=JWT_EXPIRY_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await User.get_or_none(username=username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
