# app/main.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from tortoise import Tortoise
from app.database import init
from app.routers import user, post, comment, comment_likes, likes, images
from app.auth import auth
from fastadmin import fastapi_app as admin_app
from fastadmin import register
from app.models.user import User
from environs import Env
from redis.asyncio import Redis
from starlette.middleware.sessions import SessionMiddleware
import uvloop
import asyncio
import uvicorn
import time

env = Env()
env.read_env()

DATABASE_URL = env.str("DATABASE_URL")
JWT_SECRET_KEY = env.str("JWT_SECRET_KEY")

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())





@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator:
    print(f"Starting up: Initializing {application.title}...")
    await init()
    print("Database initialized!")
    yield
    print("Shutting down: Closing database connections...")
    await Tortoise.close_connections()
    print("Database connections closed!")


app = FastAPI(
    title="Blog Post API",
    description=(
        "A robust API for managing blog posts. Users can register, create posts, leave comments, "
        "add likes, and upload images. The API supports authentication and authorization with JWT."
    ),
    version="1.0.0",
    contact={
        "name": "Matnazar Matnazarov",
        "url": "https://github.com/Matnazar-Matnazarov",
        "email": "matapi@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time-ms"] = f"{process_time:.3f} ms"
    return response


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(comment_likes.router)
app.include_router(likes.router)
app.include_router(images.router)


@app.get("/", summary="Root endpoint", description="The main endpoint of the API.")
async def root():
    return {"message": "Blog Post API - Welcome!"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        contact=app.contact,
        license_info=app.license_info,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
        "backgroundColor": "#FFFFFF",
    }
    openapi_schema["servers"] = [
        {"url": "http://127.0.0.1:8000", "description": "Local Development Server"},
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

register(
    app=admin_app,
    db_url=DATABASE_URL,
    modules=["app.models.user"],  # User modelini ro‘yxatdan o‘tkazish
    admin_models=[User],  # Admin uchun User modelini ko‘rsatish
    username_field="username",  # Foydalanuvchi nomini aniqlash uchun maydon
    password_field="password",  # Parolni aniqlash uchun maydon
)

app.add_middleware(SessionMiddleware, secret_key=JWT_SECRET_KEY)

app.mount("/admin", admin_app)

app.openapi = custom_openapi

