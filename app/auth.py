# from fastapi import APIRouter, HTTPException
# from app.schemas import UserSignup, UserLogin
# from app.database import get_user_by_email, create_user
# import secrets

# router = APIRouter()


# @router.post("/signup")
# def signup(user: UserSignup):
#     if get_user_by_email(user.email):
#         raise HTTPException(status_code=400, detail="Email already registered")
#     token = secrets.token_hex(16)
#     create_user(user.email, user.password, token)
#     return {"token": token}

# @router.post("/login")
# def login(user: UserLogin):
#     stored_user = get_user_by_email(user.email)
#     if stored_user and stored_user.password == user.password:
#         return {"token": stored_user.token}
#     raise HTTPException(status_code=401, detail="Invalid credentials")

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import UserSignup, UserLogin
from app.database import get_user_by_email, create_user, get_db
import secrets

router = APIRouter()

@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    if get_user_by_email(user.email, db):
        raise HTTPException(status_code=400, detail="Email already registered")
    token = secrets.token_hex(16)
    create_user(user.email, user.password, token, db)
    return {"token": token}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    stored_user = get_user_by_email(user.email, db)
    if stored_user and stored_user.password == user.password:
        return {"token": stored_user.token}
    raise HTTPException(status_code=401, detail="Invalid credentials")