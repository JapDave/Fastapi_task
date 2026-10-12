from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import get_db, create_post, get_posts_by_user, delete_post as remove_post
from .helpers import authenticate_token
from .schemas import PostCreate

router = APIRouter()


@router.post("", status_code=201)
def add_post(body: PostCreate, user_id: int = Depends(authenticate_token), db: Session = Depends(get_db)):
    return {"postID": create_post(body.text, user_id, db)}


@router.get("")
def list_posts(user_id: int = Depends(authenticate_token), db: Session = Depends(get_db)):
    return [{"postID": post.id, "text": post.text} for post in get_posts_by_user(user_id, db)]


@router.delete("/{post_id}")
def delete_post(post_id: int, user_id: int = Depends(authenticate_token), db: Session = Depends(get_db)):
    remove_post(post_id, user_id, db)
    return {"message": "Post deleted"}
