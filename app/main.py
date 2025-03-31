from fastapi import FastAPI
from app.database import init
from app.routers import user, post, comment, comment_likes, likes, images
from app.auth import auth

app = FastAPI(title="Blog Post API")

# Routerlarni qo‘shish
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
# Boshqa routerlarni qo‘shing...

@app.on_event("startup")
async def startup_event():
    await init()

@app.get("/")
async def root():
    return {"message": "Blog Post API"}