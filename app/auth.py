import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import create_user, get_db, get_user_by_email
from app.schemas import UserLogin, UserSignup
from app.security import hash_password, verify_password

router = APIRouter()


@router.post("/signup", status_code=201)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    if get_user_by_email(user.email, db):
        raise HTTPException(status_code=409, detail="Email already registered")
    token = secrets.token_urlsafe(32)
    try:
        create_user(user.email, hash_password(user.password), token, db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered") from None
    return {"token": token}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    stored_user = get_user_by_email(user.email, db)
    if not stored_user or not verify_password(user.password, stored_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    stored_user.token = secrets.token_urlsafe(32)
    db.commit()
    return {"token": stored_user.token}
