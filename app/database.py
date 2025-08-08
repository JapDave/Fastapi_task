from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .models import init_db, User, Post
from fastapi import HTTPException

DATABASE_URL = "sqlite:///./my_database.db"

def get_db():
    engine = create_engine(DATABASE_URL)
    session_local = Session(bind=engine)
    try:
        yield session_local
    finally:
        session_local.close()

def get_user_by_token(token: str, db: Session):
    try:
        print(token)
        return db.query(User).filter(User.token == token).one()
    except Exception as e:
        print(e,"Dsada") 
        return None

def get_user_by_email(email: str, db: Session):
    try:
        return db.query(User).filter(User.email == email).one()
    except:
        return None

def create_user(email: str, password: str, token: str, db: Session):
    user = User(email=email, password=password, token=token)
    db.add(user)
    db.commit()

def create_post(text: str, user_id: int, db: Session):
    post = Post(text=text, user_id=user_id)
    db.add(post)
    db.commit()
    return post.id

def get_posts_by_user(user_id: int, db: Session):
    return db.query(Post).filter(Post.user_id == user_id).all()

def delete_post(post_id: str, user_id: int, db: Session):
    post = db.query(Post).filter(Post.post_id == post_id, Post.user_id == user_id).first()
    if post:
        db.delete(post)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Post not found")