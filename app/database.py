import os
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, Post, User

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./my_database.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db


def get_user_by_token(token: str, db: Session):
    return db.query(User).filter(User.token == token).first()


def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def create_user(email: str, password: str, token: str, db: Session):
    user = User(email=email, password=password, token=token)
    db.add(user)
    db.commit()
    return user


def create_post(text: str, user_id: int, db: Session):
    post = Post(text=text, user_id=user_id, post_id=str(uuid4()))
    db.add(post)
    db.commit()
    return post.id


def get_posts_by_user(user_id: int, db: Session):
    return db.query(Post).filter(Post.user_id == user_id).order_by(Post.id).all()


def delete_post(post_id: int, user_id: int, db: Session):
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
