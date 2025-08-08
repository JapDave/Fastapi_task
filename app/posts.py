from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.helpers import authenticate_token
from app.schemas import PostCreate
from app.database import create_post, get_posts_by_user, get_db, get_user_by_token
from app.cache import cache

router = APIRouter()


@router.post("/addPost")
def add_post(post: PostCreate, current_user: int = Depends(authenticate_token), db: Session = Depends(get_db)):
    if len(post.json()) > 1024 * 1024:
        raise HTTPException(status_code=400, detail="Payload size too large")
    post_id = create_post(post.text, current_user, db)
    return {"postID": post_id}

@router.get("/getPosts")
def get_posts(current_user: int = Depends(authenticate_token), db: Session = Depends(get_db)):
    if current_user in cache:
        return cache[current_user]

    posts = get_posts_by_user(current_user, db)
    user_posts = [{"postID": post.id, "text": post.text} for post in posts]

    # Cache the posts
    cache[current_user] = user_posts
    return user_posts

@router.delete("/deletePost")
def delete_post(post_id: str, current_user: int = Depends(authenticate_token), db: Session = Depends(get_db)):
    
    delete_post(post_id, current_user, db)
    return {"message": "Post deleted successfully"}