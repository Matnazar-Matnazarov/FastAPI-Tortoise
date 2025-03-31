# app/main.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from tortoise import Tortoise
from app.database import init
from app.routers import user, post, comment, comment_likes, likes, images
from app.auth import auth


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
        "name": "Matnazar Aromatization",
        "url": "https://github.com/Matnazar-Matnazarov",
        "email": "matnazar@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

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


app.openapi = custom_openapi
