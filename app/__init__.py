from contextlib import asynccontextmanager

from fastapi import FastAPI

from .auth import router as auth_router
from .database import Base, engine
from .posts import router as posts_router


@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="FastAPI Blogging API", lifespan=lifespan)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(posts_router, prefix="/posts", tags=["Posts"])
